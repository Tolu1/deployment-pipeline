# Module for pipelining GitHub to Development Server e.g AWS
import json
from getpass import getpass
from github import Github
import requests

class AWSPipeline():

    def __init__(self, repo, branch) -> None:
        self.repo = repo
        self.branch = branch
        
    def set(self, repo, branch):
        self.repo = repo
        self.branch = branch

    def install(self, command, aws_server_url):
        headers = {'Content-Type': 'application/json'}
        data = {
            'repo': f'{self.repo}',
            'branch': f'{self.branch}',
            'run_command': f'{command}'
        }
        data = json.dumps(data)
        resp = requests.post(url=aws_server_url, data=data, headers=headers)
        resp = resp.json()
        return resp.get('status'), resp.get('message')
        # if resp.get('status') == 'success':
        #     return 'success'
        # elif resp.get('status') == 'error':
        #     return resp.get('message')

class Authenticator():

    @classmethod
    def run(cls):
        print('**Authentication required for GitHub pipelining**')
        Username = input('username: ')
        Password = getpass('password: ')
        git = Github(Username, Password)
        repos = git.get_repos(type='all')
        print(repos)


    @classmethod
    def is_authenticated(self):
        pass

def createPipeline(hosting_platform='aws', repo=None, branch=None):
    print('='*50)
    print(' '*5 + f'GitHub to {hosting_platform.upper()} Pipeline (Development)')
    print('-'*50)

    if repo is None:
        repo = input('RepoName: ')
        manual_message = '''You can go over to GitHub and create a webhook on your repo \
    For more info visit to https://docs.github.com/en/developers/webhooks-and-events/webhooks/creating-webhooks
        '''
        while True:
            choice = input('Do you want to automatically create web hook on repo(y/N): ') 
            if choice == 'y':
                print('[ERROR] Automatic Webhooks not yet supported, you must create a webhook on Githubby yourself')
                print(manual_message)
                break
            elif choice == 'N':
                print(manual_message)
                break
            elif choice not in ['y', 'N']:
                print('Please choose a valid option')
        print()
        # Automatic webhooks are not currently supported so we don't need to authenticate
        if False:
            Authenticator.run()
    if branch is None:
        print("[Warning] Branch is not defined --> using 'main' as default branch")  
        branch = 'main'  

    if hosting_platform == 'aws':
        aws = AWSPipeline(repo=repo, branch=branch)
        return aws

 