import json
import os
from typing import Any, Dict, Tuple, Optional
import semver

import utils
import outputs
from shared_packages import markdown
from shared_packages.repository_manager import RepositoryManager
from shared_packages.notifications_service import NotificationsService
from shared_packages.sirrend_config import SirrendConfig
from shared_packages.container_registries_handler import ContainerRegistryHandler
from shared_packages.helm.client import HelmCLI as Helm, HelmCommandSyntaxError, HelmCommandExecutionError
from shared_packages.sirrend_logger import SirrendLogger
from shared_packages.utils import Utils
from shared_packages.helm_upgrade_manager import (
    HelmUpgradeManager, NoMoreMinorsError, NoMoreMajorsError)

headers = {
    "Access-Control-Allow-Headers": "Content-Type",
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
}
logger = SirrendLogger.configure_logger(SirrendLogger.INFO)


def handle_upgrade_errors(
        config: SirrendConfig, chart_name: str, current_version: str, error: Exception, customer: str) -> Dict[str, Any]:
    """
    Handles the NoMoreVersions error types by sending corresponding Teams messages.

    :param config: The configuration object containing settings.
    :param chart_name: Name of the Helm chart.
    :param current_version: Current version of the Helm chart.
    :param error: The caught error instance to handle.
    :param customer: The customer to send the notification to.
    :return: A dictionary indicating the status code and possibly a message.
    """
    message = markdown.Form(markdown.Form.TEAMS_DIALECT)
    if isinstance(error, NoMoreMajorsError):
        notification_message = (
            f"🎉 Great news! Your chart, `{chart_name}` at version `{current_version}`, "
            "is the latest - it's completely up to date! 🌟"
        )
    elif isinstance(error, NoMoreMinorsError):
        notification_message = (
            f"🌈 Heads up! You've reached the last minor version for `{chart_name}`. Exciting times! 🚀 "
            "For more updates, consider enabling the `upgrade_majors` option in your `sirrend.cfg` file "
            "to keep the upgrade going!"
        )
    else:
        return {'statusCode': 500, 'headers': headers}

    if config.notifications_enabled:
        NotificationsService().send(message.new_line(notification_message).full_form)
        logger.info(f"Sent the following {config.notifications_type} message to {customer}: {notification_message}")
        return {'message': f"Sent the following {config.notifications_type} message to {customer}: {notification_message}",
                'statusCode': 200, 'headers': headers}

    return {'statusCode': 200, 'headers': headers}


def handle_target_version_warnings(
        config: SirrendConfig, chart_name: str, current_version: str, target_version: str, customer: str
) -> Optional[Dict[str, Any]]:
    """
    Handles requested target version warnings.

    :param config: The configuration object containing settings.
    :param chart_name: Name of the Helm chart.
    :param current_version: Current version of the Helm chart.
    :param target_version: The requested chart version
    :param customer: The customer to send the notification to.
    :return: A dictionary indicating the status code and a message or None.
    """
    if target_version is None:
        return None

    message = markdown.Form(markdown.Form.TEAMS_DIALECT)
    versions_comparison_result = semver.compare(current_version, target_version)
    if versions_comparison_result >= 0:
        if versions_comparison_result == 0:
            notification_message = (f"The requested Chart version for {chart_name} is the same as "
                                    f"the current Chart version -> {current_version}")
        else:
            notification_message = (f"The requested Chart version for {chart_name} is a downgrade of the current Chart "
                                    f"version ({current_version} -> {target_version}), which we don't yet support.")

        if config.notifications_enabled:
            NotificationsService().send(
                message.new_line(notification_message).full_form)
            logger.info(f"Sent the following {config.notifications_type} message to {customer}: {notification_message}")
            return {'message': f"Sent the following {config.notifications_type} message to {customer}: {notification_message}",
                    'statusCode': 200, 'headers': headers}

        return {'message': notification_message, 'statusCode': 200, 'headers': headers}

    return None


def perform_post_upgrade_tasks(
        helm: HelmUpgradeManager, config: SirrendConfig, repo: Any, data: utils.Item, current_version: str,
        target_version: str, new_branch: str) -> str:
    """
    Performs all post upgrade tasks according to the client's sirrend.cfg file, which includes opening a GitHub PR,
    opening a Jira ticket, and sending a Teams message.

    :param helm: Instance of HelmUpgradeManager.
    :param config: Configuration settings from sirrend.cfg.
    :param repo: RepositoryManager instance.
    :param data: Extracted event data containing chart and repository details.
    :param current_version: The current chart version before upgrade.
    :param target_version: The target chart version after upgrade.
    :param new_branch: The name of the new branch for the upgrade.
    :return: The URL of the opened PR.
    """
    current_score, target_score = None, None
    if helm.metadata.classification == helm.metadata.COMMUNITY:
        current_score, target_score = fetch_security_scores(helm, data.chart_name, current_version, target_version)

    # find CRD yaml files outside the templates dir
    files = repo.find_commit_changed_files_by_branch(new_branch)
    files = [file.removeprefix(data.chart_path) for file in files]
    _, files = helm.handler.have_files_outside_templates(files)

    files = [repo.local_path + "/" + data.chart_path + file for file in files]
    crds = []
    for file in files:
        if helm.handler.is_crd_manifest(file):
            crds.append(file.removeprefix(os.path.join(repo.local_path, data.chart_path)))

    files = crds
    artifact_hub_url = helm.handler.get_chart_artifact_hub_link()

    # get list of images used in the chart
    template = Helm().template(helm.metadata.dir)
    customer_defined_images = ContainerRegistryHandler.get_safecash_images_from_helm_template(template)

    # create PR description and open
    pr_mrkdwn_description = outputs.pr_description_markdown(
        target_version, helm.new_chart_handler.chart_metadata.appVersion,
        customer_defined_images, current_score, target_score, files, artifact_hub_url)
    pr_url = repo.open_pr(
        new_branch, title=f"Sirrend/{data.chart_name}/{target_version}", mrkdwn_body=pr_mrkdwn_description)

    if config.jira_enabled:
        outputs.open_jira_task(
            data.customer, pr_url, repo.repo_name, data.chart_name, current_version, target_version,
            customer_defined_images, current_score, target_score, files, artifact_hub_url)

    if config.notifications_enabled:
        outputs.send_new_pr_notification(data, pr_url, current_version, target_version)

    return pr_url


def fetch_security_scores(helm: Any, chart_name: str, current_version: str, target_version: str) -> Tuple[int, int]:
    """
    Fetch security scores of the chart versions in context.

    :param helm: Instance of HelmUpgradeManager containing metadata.
    :param chart_name: Name of the chart being upgraded.
    :param current_version: Current version of the chart.
    :param target_version: Target version to upgrade to.
    :return: A tuple containing the current and target security scores.
    """
    current_score = utils.fetch_chart_security_score(
        helm.metadata.repository, chart_name, current_version, helm.metadata.name)
    target_score = utils.fetch_chart_security_score(
        helm.metadata.repository, chart_name, target_version, helm.metadata.name)

    return current_score, target_score


def is_invalid_chart(config: SirrendConfig, local_chart_path: str, data: any) -> Optional[Dict[str, any]]:
    try:
        Helm().template(local_chart_path)
    except (HelmCommandSyntaxError, HelmCommandExecutionError):
        if config.notifications_enabled:
            NotificationsService().send(
                message_text=f"# ⛔ Heads up! ⛔ </br></br>"
                             f""
                             f"We are unable to template `{data['chart_name']}` at `/{data['chart_path']}`. "
                             f"Please check its validity and let us know if it is correct!")

            logger.warning("Sent a {config.notifications_type} message to notify the client about a badly formed helm chart.")
            return {
                'message': "Sent a {config.notifications_type} message to notify the client about a badly formed helm chart.",
                'statusCode': 200, 'headers': headers}
        return {
            'message': f"Badly formed helm chart: {data['chart_name']}.", 'statusCode': 200, 'headers': headers}

    return None


def main_handler(item: utils.Item) -> dict:
    data = utils.extract_event_data(item)
    if not data:
        logger.error("Failed to extract event data.")
        return {
            'message': "Failed to extract event data.",
            'statusCode': 500,
            'body': json.dumps(data),
            'headers': headers
        }

    # get customer data
    customer_data = utils.get_repo_details(data.clone_url)
    repo = RepositoryManager(
        repo_url=customer_data["repo_url"], token=customer_data["token"], webhook_branch=data.branch)

    # create new branch
    new_branch = utils.dynamic_branch_name()
    repo.create_new_branch(new_branch)

    local_chart_path = os.path.join(repo.local_path, data.chart_path)
    current_version = utils.extract_version(local_chart_path)

    if current_version is None:
        logger.error("Failed to find Chart.yaml in the local chart dir: {local_chart_path}.")
        return {
            'message': f"Failed to find Chart.yaml in the local chart dir: {local_chart_path}.",
            'statusCode': 500,
            'headers': headers
        }

    config = SirrendConfig()
    warn = handle_target_version_warnings(
        config, data.chart_name, current_version, data.target_version, data.customer)
    if warn is not None:
        return warn

    # test chart validity
    invalid = is_invalid_chart(config, local_chart_path, data)
    if invalid is not None:
        return invalid

    # initiate upgrade
    try:
        helm = HelmUpgradeManager(client_chart_dir=local_chart_path, target_version=data.target_version)
        helm.Upgrade()
    except (NoMoreMajorsError, NoMoreMinorsError, HelmCommandSyntaxError, HelmCommandExecutionError) as e:
        return handle_upgrade_errors(config, data.chart_name, current_version, e, data.customer)

    target_version = utils.extract_version(local_chart_path)
    if current_version is None:
        logger.error("Failed to find Chart.yaml in the upgraded local chart dir. Something went wrong during the "
                     "upgrade process.")
        return {
            'message': "Failed to find Chart.yaml in the upgraded local chart dir. "
                       "Something went wrong during the upgrade process.",
            'statusCode': 500,
            'headers': headers
        }

    pr_url = None
    if repo.commit_and_push(new_branch):
        pr_url = perform_post_upgrade_tasks(helm, config, repo, data, current_version, target_version, new_branch)

    Utils.cleanup_directory(repo.local_path)

    logger.success("Upgrade was a success!")
    return {
        'message': f"Succeeded in upgrading {data.chart_name} from {current_version} to {target_version}.",
        'pr_url': f"{pr_url}",
        'statusCode': 200,
        'headers': headers
    }
