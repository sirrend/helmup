from typing import Dict
from github import Github
from github import Auth
import yaml
from packages import commons
from shared_packages.sirrend_logger import SirrendLogger

logger = SirrendLogger.configure_logger(SirrendLogger.INFO)


# class Utils:
#     @classmethod
#     def find_helm_charts(cls) -> Dict[str, str]:
#         charts: Dict[str, str] = {}
#         csv = commons.CSV_FILE_NAME
#         rows = csv.get_rows()

#         for row in rows:
#             logger.info(rows)
#             if len(row) > 0:
#                 charts[row[0]] = row[-1].replace("/Chart.yaml", "")

#         return charts

class GitHubScraper():
    
    def __init__(self, repo_owner, repo_name, github_token):
        logger.info(f"Starting to scrape the {repo_owner}/{repo_name} repository")
        g = Github(github_token)
        # Get the repository object
        self.repo = g.get_repo(f"{repo_owner}/{repo_name}")
    
    def scrape_git_repo(self):
        """
        Scrape the given git repository. Iterate over all the files in the repo.
        For every file named "Chart.yaml" fill a gitDict , and append to a list.
        
        :param repo_owner: (str) The name of the Github repo owner.
        :param repo_name: (str) The name of the Github repo.
        :param secret_name: (str) The secret name in AWS to retreive.
        
        :return gitDict[]: List of dictionaries "gitDict"
        """
        gitDictList = []
        contents = self.repo.get_contents("")
        while contents:
            file_content = contents.pop(0)
            #TODO : Find more generic solution, this one is SC tailored
            if "/charts" in file_content.path:
                continue
            if file_content.type == "dir":
                contents.extend(self.repo.get_contents(file_content.path))
            else:
                if file_content.name == "Chart.yaml":
                    gitDict = {
                        "chart_name": "",
                        "link_to_github": "",
                        "chart_version": "",
                        "app_version": "",
                        "security_level": "",
                        "Path" : "",
                    }
                    logger.info(f"Found a new Chart.yaml file on location {file_content.path}")
                    yamlFile = file_content.decoded_content.decode('utf-8')
                    # Load the YAML content
                    yaml_content = yaml.safe_load(yamlFile)
                    gitDict["Path"] = file_content.path
                    gitDict["chart_name"] = yaml_content['name']
                    gitDict["link_to_github"] = file_content.html_url
                    gitDict["chart_version"] = yaml_content['version']
                    try:
                        gitDict["app_version"] = yaml_content['appVersion']
                    except:
                        gitDict["app_version"] = '0.0.0'
                    gitDict["security_level"] = "N/A"
                    logger.info(f"Chart name: {yaml_content['name']}\n Link to Github: {gitDict['link_to_github']}\n Version: {gitDict['chart_version']}\n App Version: {gitDict['app_version']}")
                    gitDictList.append(gitDict)
        return gitDictList
                    
def main():
    g = GitHubScraper("sirrend", "kuba_test", commons.GITHUB_TOKEN)
    g.scrape_git_repo()
    
if __name__=="__main__":
    main()