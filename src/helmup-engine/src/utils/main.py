import os.path
import string
import json
import secrets as Secrets
import yaml
import commons
from pydantic import BaseModel
from typing import Optional
from shared_packages.chart_security_score import ChartSecurityScore, WrongChartNameError
from shared_packages.sirrend_logger import SirrendLogger

logger = SirrendLogger.configure_logger(SirrendLogger.INFO)


class Item(BaseModel):
    customer: str
    clone_url: str
    branch: str
    chart_name: str
    chart_path: str
    target_version: Optional[str] = None


def extract_event_data(item: Item) -> Item:
    """
    Extract relevant data from the trigger event, checking if data is within a 'body' key.

    :param event: (dict) The event payload.
    :return: A dictionary containing relevant event data.
    """
    try:
        if all(attr is not None for attr in [item.customer, item.clone_url, item.branch, item.chart_name, item.chart_path]):
            logger.info(f"Event data: {item}")
            return item
        else:
            logger.error(f"Incomplete or missing data in the event: {json.dumps(event)}")
            exit(1)
    except json.JSONDecodeError:
        logger.error("Invalid JSON in the event body, exiting.")
        exit(1)


def dynamic_branch_name() -> str:
    """
    Creates a dynamic branch name using a unique hash.
    """
    # create hash to branch naming
    characters = string.ascii_letters + string.digits
    git_hash = ''.join(Secrets.choice(characters) for _ in range(6))

    return f"sirrend/upgrade_helm_chart_{git_hash}"


def get_repo_details(clone_url: str) -> dict:
    """
    Get all environment variables needed for this program to run.

    :param customer: (str) teh customer name.
    :param clone_url: (str) the repository to clone.
    :returns: a dict containing the needed repository data.
    """
    repo_url = clone_url.replace("https://github.com/", "").replace(".git", "")

    return {
        "repo_url": repo_url,
        "token": commons.GITHUB_TOKEN
    }


def extract_version(chart_local_dir: str) -> str | None:
    """
    Extracts the current version of the customer Helm Chart.

    :param chart_local_dir: local path to the chart.
    :return: the chart version specified under Chart.yaml.
    """
    chart_yaml = os.path.join(chart_local_dir, "Chart.yaml")
    if os.path.exists(chart_yaml):
        with open(chart_yaml) as chart:
            data = yaml.safe_load(chart)
            return data["version"]

    return None


def fetch_chart_security_score(repository, chart_name, version, fallback_name):
    """
    Fetch a chart security score from ArtifactHub.


    """
    try:
        return ChartSecurityScore.fetch_score(repository, chart_name, version)
    except WrongChartNameError:
        logger.warning("Failed to fetch chart score, trying again with the Chart.yaml name variable.")
        return ChartSecurityScore.fetch_score(repository, fallback_name, version)
