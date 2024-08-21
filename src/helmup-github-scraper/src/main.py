import os.path

from packages.utils import GitHubScraper
from packages import commons
from packages.title_handler import TitleHandler
from shared_packages.repository_manager import RepositoryManager
from shared_packages.sirrend_logger import SirrendLogger
import requests
import json

logger = SirrendLogger.configure_logger(SirrendLogger.INFO)
headers = {
    'Content-Type': 'application/json'
}

def trigger_helmup_engine(chart_name, chart_dir):
    payload = {
        "customer": commons.CUSTOMER_NAME,
        "clone_url": commons.GIT_REPOSITORY_URL,
        "branch": commons.GIT_BRANCH,
        "chart_name": chart_name,
        "chart_path": chart_dir
    }
    full_svc_url = commons.HELMUP_SVC_URL + '/upgrade'
    if not full_svc_url.startswith('http://'):
        full_svc_url = 'http://' + commons.HELMUP_SVC_URL + '/upgrade'
    logger.info(f"Starting to trigger helmup service at URL: {full_svc_url}") 
    logger.info(f"The payload sent to the service: {payload}")
    try:
        response = requests.post(full_svc_url, data=json.dumps(payload), headers=headers)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
        logger.info(f'Status Code: {response.status_code}')
        logger.info(f'Response: {response.json()}')
    except requests.exceptions.HTTPError as http_err:
        logger.error(f'HTTP error occurred: {http_err}')  # HTTP error
    except Exception as err:
        logger.error(f'Other error occurred: {err}')  # Other errors  

def main():
    """
    Main lambda function.

    :param event: from lambda.
    :param context: from context.
    """
    # create repo instance
    r = RepositoryManager(repo_url=commons.GIT_REPOSITORY_URL, token=commons.GITHUB_TOKEN)
    prs = r.get_open_prs()

    # search for helm chart folders
    
    scraper = GitHubScraper(commons.CUSTOMER_NAME, commons.GIT_REPOSITORY_NAME, commons.GITHUB_TOKEN)
    gitDict = scraper.scrape_git_repo()
    logger.info(gitDict)
    
    # filter out already in latest charts

    for dict in gitDict:
        logger.info(F"Starting to analyze chart {dict["chart_name"]}")
        pr_exist = False
        print(pr_exist)
        for pr in prs:
            title = pr.title
            title_chart_name, _ = TitleHandler.pr_title_data_extract(title)

            if title_chart_name.lower() == dict["chart_name"]:
                logger.warning(f"Found an open PR for {dict["chart_name"]}, moving on.")
                pr_exist = True
                break

        if not pr_exist:
            chart_dir = f"/tmp/{commons.CUSTOMER_NAME}-{commons.GIT_REPOSITORY_NAME}/{dict["chart_name"]}"
            # if os.path.exists(os.path.join(r.local_path, chart_dir)):
            logger.info(f"Opening PR for {dict["chart_name"]}")
            trigger_helmup_engine(dict["chart_name"], chart_dir)
                    
if __name__=="__main__":
    main()