import os

class TokenRetriever:
    @staticmethod
    def get_pat():
        # Chain of responsibility for PAT retrieval
        pat = os.environ.get('GITHUB_PAT')
        if pat:
            return pat
        
        try:
            with open('.github_pat', 'r') as f:
                return f.read().strip()
        except FileNotFoundError:
            raise ValueError("No GitHub PAT found in environment or .github_pat file")