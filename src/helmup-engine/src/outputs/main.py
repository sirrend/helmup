from typing import Optional

from shared_packages.notifications_service import NotificationsService

import commons, utils
from shared_packages.jira import JiraTicketCreator
from shared_packages.chart_security_score import SecurityScore
from shared_packages.sirrend_logger import SirrendLogger
from shared_packages import markdown
import emoji

logger = SirrendLogger.configure_logger()


def open_jira_task(
        customer: str, link: str, repo_name: str, chart_name: str,
        current_chart_version: str, new_chart_version: str,
        customer_defined_images: list[str],
        current_score: Optional[SecurityScore] = None,
        target_score: Optional[SecurityScore] = None,
        orphan_files: Optional[list[str]] = None,
        artifact_hub_link: Optional[str] = None):
    """
    Open a jira ticket about the opened PR.

    :param (str) customer: the customer name.
    :param (str) link: the PR link to append to the issue's description.
    :param (str) repo_name: the repository in context.
    :param (str) chart_name: The chart name.
    :param (str) current_chart_version: The current customer chart version.
    :param (str) new_chart_version: the new chart version.
    :param (list[str]) customer_defined_images: the customer self defined images.
    :param (SecurityScore | None) current_score: the current vulnerability severity.
    :param (SecurityScore | None) target_score: the target version vulnerability severity.
    :param (list[str] | None) orphan_files: files which where found outside the `templates` dir.
    :param (str | None) artifact_hub_link: the link to read in about the files found outside of templates dir.
    """
    jira = JiraTicketCreator()
    epic_key = jira.create_epic()

    # find custom fields by name (get from client somehow)
    fields = jira.get_custom_fields(["Epic Link"])
    custom_fields = {
        fields["Epic Link"]: epic_key
    }

    # extract pull request ID
    pr_id = link.split("/")[-1]

    # build markdown message
    issue_mrkdwn = markdown.Form(markdown.Form.JIRA_DIALECT)

    if current_score is not None:
        current_score_text = (
                issue_mrkdwn.bold(
                    f"Current Image Vulnerability Severity Level:", False) +
                issue_mrkdwn.jira_colorized_text(
                    current_score.string_grade, current_score.get_score_color()))
    else:
        current_score_text = (
            issue_mrkdwn.bold(
                f"Current image has no vulnerability severity level which can be fetched:", False))
    if target_score is not None:
        target_score_text = (
                issue_mrkdwn.bold(
                    f"Target Image Vulnerability Severity Level:", False) +
                issue_mrkdwn.jira_colorized_text(
                    target_score.string_grade, target_score.get_score_color()))
    else:
        target_score_text = (
            issue_mrkdwn.bold(
                f"Current image has no vulnerability severity level which can be fetched:", False))

    # Construct a message about private images detection with an optional list of customer-defined images.
    warning_emoji = emoji.emojize(':warning:', language="en")
    customer_private_images = (
        (issue_mrkdwn.bold(f"{warning_emoji}️  Private Images Detected", True) +
         "It's important that you upgrade your local image before upgrading this chart!\n" +
         issue_mrkdwn.dotted_list(customer_defined_images)) if len(customer_defined_images) > 0 else ""
    )

    issue_mrkdwn.new_line(
        issue_mrkdwn.bold("Details:", False) + " A new Helm chart upgrade PR is available for overview."
    ).new_line(
        issue_mrkdwn.bold("Repository:", False) + f" {repo_name}"
    ).new_line(
        issue_mrkdwn.bold("Modified Chart:", False) + f" {chart_name}"
    ).new_line(
        issue_mrkdwn.bold("Version Upgrade:", False) + f" {current_chart_version} -> {new_chart_version}"
    ).new_line(
        "\n"
    ).new_line(
        current_score_text
    ).new_line(
        target_score_text
    ).new_line(
        "\n"
    ).new_line(
        customer_private_images
    ).new_line(
        "Important - Read Before Upgrade!\n" +
        "Found the following CRDs outside the templates dir: \n" +
        issue_mrkdwn.dotted_list(orphan_files) +
        "\n\n We recommend visiting the " +
        issue_mrkdwn.link("Community Charts page", artifact_hub_link, False) +
        " to determine if further upgrade actions are required on your part. \n" if len(orphan_files) > 0 else "\n"
    ).new_line(
        issue_mrkdwn.link("Click me to Upgrade!", link)
    ).new_section(
        issue_mrkdwn.embed_image(
            commons.JIRA_BACKGROUND_IMAGE,
            width=JiraTicketCreator.HELM_BACKGROUND_WIDTH,
            height=JiraTicketCreator.HELM_BACKGROUND_HEIGHT)
    )

    res = jira.create_ticket(
        issue_type="Task",
        summary=f"Sirrend PR Overview - {repo_name} - #{pr_id}",
        description=issue_mrkdwn.full_form,
        image_to_embed=JiraTicketCreator.HELM_BACKGROUND_IMAGE,
        custom_fields=custom_fields)

    logger.info(f"Ticket creation result: {res}")


def pr_description_markdown(
        target_version: str,
        target_app_version: str,
        customer_defined_images: list[str],
        current_score: SecurityScore | None = None,
        target_score: SecurityScore | None = None,
        orphan_files: Optional[list[str]] = None,
        artifact_hub_link: Optional[str] = None) -> str:
    """
    Creates the PR (Pull Request) description in Markdown.

    :param target_version: The chart target version.
    :param target_app_version: The chart target app version.
    :param (list[str]) customer_defined_images: the customer self defined images.
    :param (SecurityScore | None) current_score: the current vulnerability severity.
    :param (SecurityScore | None) target_score: the target version vulnerability severity.
    :param (list[str] | None) orphan_files: files which where found outside the `templates` dir.
    :param (str | None) artifact_hub_link: the link to read in about the files found outside of templates dir.
    """
    markdown_form = markdown.Form()

    # Generating score badges
    current_score_badge = (markdown_form.bold(current_score.get_badge(False), False)
                           if current_score is not None
                           else "Couldn't find severity score for the current chart in ArtifactHub.\n")
    target_score_badge = (markdown_form.bold(target_score.get_badge(True), False)
                          if target_score is not None
                          else "Couldn't find severity score for the target chart in ArtifactHub.\n")

    # generating private images section

    warning_emoji = emoji.emojize(':warning:', language="en")
    # Construct a message about private images detection with an optional list of customer-defined images.
    customer_private_images = (
        (markdown_form.bold(f"{warning_emoji}️  Private Images Detected", True) +
         "It's important that you upgrade your local image before upgrading this chart!\n" +
         markdown_form.dotted_list(customer_defined_images)) if len(customer_defined_images) > 0 else ""
    )

    # Building the PR description
    pr_description = (
        markdown_form.new_titled_section(
            markdown_form.bold("PR Purpose:", False),
            markdown_form.italic(
                f"Upgrade the helm chart version to {target_version} with the app version set to {target_app_version}",
                True),
            markdown_form.separator(),
            title="Helm Chart Upgrade Details"
        ).new_titled_section(
            current_score_badge,
            target_score_badge,
            "\n",
            customer_private_images,
            markdown_form.separator(),
            title="Chart Images Breakdown",
            title_size=3
        )
    )

    if len(orphan_files) > 0:
        pr_description.new_titled_section(
            "Found the following CRDs outside the templates dir: \n" +
            markdown_form.dotted_list(orphan_files) + "\n\n" +
            markdown_form.bold("We recommend visiting the " +
                               markdown_form.link("Community Charts page", artifact_hub_link, False) +
                               " to determine if further upgrade actions are required on your part."),
            title="--- Important - Read Before Upgrade! ---",
            title_size=2
        )

    pr_description.new_section(markdown_form.italic("Upgraded by Sirrend Ltd.", False))

    return pr_description.full_form


def send_new_pr_notification(data: utils.Item, pr_url: str, current_version: str, target_version: str) -> None:
    """
    Send a Teams notification about the new PR.

    :param data: Extracted event data containing chart and repository details.
    :param pr_url: URL of the pull request to include in the notification.
    :param current_version: The current version of the chart.
    :param target_version: The target version of the chart after upgrade.
    """
    message = markdown.Form(markdown.Form.TEAMS_DIALECT)
    NotificationsService().send(
        message.new_line(
            f"✨ {message.bold('Exciting Update:', False)} A fresh Helm Upgrade PR for `{data.chart_name}`, "
            f"moving from `{current_version}` "
            f"to `{target_version}` is ready for you to review!"
        ).new_line(
            f"\n🌟 Click " + message.link("here", pr_url) +
            " to explore the latest enhancements. Dive in now! 🚀"
        ).full_form
    )