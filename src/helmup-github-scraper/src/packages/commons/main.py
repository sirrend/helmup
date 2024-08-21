import os

# Define the list of required environment variables
required_env_vars = [
    'CUSTOMER_NAME',
    'HELMUP_SVC_URL',
    'GITHUB_TOKEN',
    'GIT_REPOSITORY_NAME',
    'GIT_BRANCH',
    'GIT_REPOSITORY_URL'
]

# Dictionary to store environment variables
env_vars = {}

# Check each required environment variable
missing_vars = []
for var in required_env_vars:
    value = os.getenv(var)
    if value is None:
        missing_vars.append(var)
    else:
        env_vars[var] = value

# If there are missing variables, raise an error
if missing_vars:
    raise EnvironmentError(f"Missing required environment variables: {', '.join(missing_vars)}")

# Print each environment variable name and its value
for var, value in env_vars.items():
    print(f"{var}: {value}")

# Assign the environment variables to your variables
CUSTOMER_NAME = env_vars['CUSTOMER_NAME']
HELMUP_SVC_URL = env_vars['HELMUP_SVC_URL']
GITHUB_TOKEN = env_vars['GITHUB_TOKEN']
GIT_REPOSITORY_NAME = env_vars['GIT_REPOSITORY_NAME']
GIT_BRANCH = env_vars['GIT_BRANCH']
GIT_REPOSITORY_URL = env_vars['GIT_REPOSITORY_URL']

# Define the CSV file name
CSV_FILE_NAME = 'backend_csv.csv'
