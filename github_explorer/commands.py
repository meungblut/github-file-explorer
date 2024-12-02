import os
import base64
from github import Github, GithubException
import requests

class Command:
    def execute(self):
        raise NotImplementedError("Subclasses must implement this method")

class FindExcelFilesCommand(Command):
    def __init__(self, org_name, max_depth=5):
        self.org_name = org_name
        self.max_depth = max_depth

    def execute(self, github_instance):
        query = f"""
        query {{  
          search(query: "org:{self.org_name} extension:xlsx OR extension:xls", type: REPOSITORY, first: 100) {{
            edges {{
              node {{
                ... on Repository {{
                  name
                  url
                  defaultBranchRef {{
                    target {{
                      ... on Commit {{
                        tree {{
                          entries {{
                            path
                            type
                          }}
                        }}
                      }}
                    }}
              }}
            }}
          }}
        }}
        """

        headers = {
            'Authorization': f'Bearer {github_instance.get_pat()}',
            'Content-Type': 'application/json'
        }

        response = requests.post('https://api.github.com/graphql', json={'query': query}, headers=headers)
        response.raise_for_status()

        excel_files = []
        for repo in response.json()['data']['search']['edges']:
            repo_name = repo['node']['name']
            
        return excel_files

class DownloadExcelFilesCommand(Command):
    def __init__(self, org_name, output_dir='excel_files'):
        self.org_name = org_name
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def execute(self, github_instance):
        g = github_instance
        org = g.get_organization(self.org_name)
        
        downloaded_files = []
        for repo in org.get_repos():
            repo_output_dir = os.path.join(self.output_dir, repo.name)
            os.makedirs(repo_output_dir, exist_ok=True)
            
            for content in repo.get_contents(""):
                if content.path.lower().endswith(('.xlsx', '.xls')):
                    file_path = os.path.join(repo_output_dir, os.path.basename(content.path))
                    with open(file_path, 'wb') as f:
                        f.write(content.decoded_content)
                    downloaded_files.append(file_path)
        
        return downloaded_files

class GithubClient:
    def __init__(self, pat=None):
        from .config import TokenRetriever
        self.pat = pat or TokenRetriever.get_pat()
        self.client = Github(self.pat)
    
    def get_pat(self):
        return self.pat
    
    def execute_command(self, command):
        return command.execute(self)