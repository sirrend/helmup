from os import putenv, error, getenv, path
from shared_packages.jira import JiraTicketCreator

# constants
ROOT_REPOSITORIES_PATH = "/tmp"
OPENAI_API_TYPE = "gpt-4-1106-preview"

# location of the background image in the Jira module
JIRA_BACKGROUND_IMAGE = path.basename(JiraTicketCreator.HELM_BACKGROUND_IMAGE)

try:
    putenv("OPENAI_MODEL", OPENAI_API_TYPE)
    putenv("ROOT_REPOSITORIES_PATH", ROOT_REPOSITORIES_PATH)
except error as err:
    print("Couldn't set the OPENAI_MODEL environment variable for the gpt_cost_calculator library use.")


GITHUB_TOKEN = getenv("GITHUB_TOKEN", None)
if GITHUB_TOKEN is None:
    raise OSError(1, "GITHUB_TOKEN env var can't be empty")

