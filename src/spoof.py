import os
import tempfile
import boto3
from git import Repo
from git.exc import GitCommandError

def run(event, context):
    # Assume API keys are stored in AWS Secrets Manager
    secrets = boto3.client('secretsmanager').get_secret_value(SecretId='github')
    secrets = eval(secrets['SecretString'])

    username = secrets['username']
    password = secrets['password']
    repo_name = 'your-repo-name'
    file_name = 'your-file-name'
    message = 'Automated commit message'

    # Clone the repo
    temp_dir = tempfile.mkdtemp()
    repo = Repo.clone_from(f'https://{username}:{password}@github.com/{username}/{repo_name}.git', temp_dir)

    # Modify the file
    with open(f'{temp_dir}/{file_name}', 'a') as f:
        f.write('\nAdded by AWS Lambda function.')

    try:
        # Commit the changes
        repo.git.add('--all')
        repo.git.commit('-m', message)

        # Push the changes
        repo.git.push()
    except GitCommandError as e:
        print(f'Error: {e}')
