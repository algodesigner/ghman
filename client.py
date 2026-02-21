import os
import sys
import json
from pathlib import Path
from github import Github, GithubException

CONFIG_DIR = Path.home() / ".ghman"
CONFIG_FILE = CONFIG_DIR / "config.json"

class GitHubClient:
    def __init__(self):
        self.token = self._load_token()
        if not self.token:
            print(
                "Error: GitHub token not found. Set GITHUB_TOKEN environment "
                "variable or run './ghman.py auth'."
            )
            sys.exit(1)
        self.gh = Github(self.token)
        try:
            self.user = self.gh.get_user()
            # Trigger a simple call to verify token
            _ = self.user.login
        except GithubException as e:
            print(f"Error: Invalid GitHub token or API error: {e}")
            sys.exit(1)

    def list_repositories(self):
        """Lists all repositories for the authenticated user."""
        try:
            repos = self.user.get_repos()
            return [repo.full_name for repo in repos]
        except GithubException as e:
            print(f"Error listing repositories: {e}")
            return []

    def create_repository(self, name, private=True):
        """Creates a new repository on GitHub."""
        try:
            repo = self.user.create_repo(name, private=private)
            return repo
        except GithubException as e:
            if e.status == 422: # Unprocessable Entity, likely already exists
                return None
            print(f"Error creating repository: {e}")
            raise e

    def get_repository(self, name):
        """Gets a repository by name."""
        try:
            return self.user.get_repo(name)
        except GithubException:
            return None

    def delete_repository(self, name):
        """Deletes a repository from GitHub."""
        try:
            repo = self.user.get_repo(name)
            repo.delete()
            return True
        except GithubException as e:
            print(f"Error deleting repository: {e}")
            return False

    def _load_token(self):
        """Loads the token from environment or config file."""
        # 1. Check environment variable
        token = os.getenv("GITHUB_TOKEN")
        if token:
            return token

        # 2. Check config file
        if CONFIG_FILE.exists():
            try:
                with open(CONFIG_FILE, "r") as f:
                    data = json.load(f)
                    return data.get("github_token")
            except (json.JSONDecodeError, IOError):
                pass
        return None

    @staticmethod
    def save_token(token):
        """Saves the token to the config file safely."""
        try:
            CONFIG_DIR.mkdir(parents=True, exist_ok=True)
            # Restrict permissions for the directory
            os.chmod(CONFIG_DIR, 0o700)
            
            with open(CONFIG_FILE, "w") as f:
                json.dump({"github_token": token}, f)
            
            # Restrict permissions for the file
            os.chmod(CONFIG_FILE, 0o600)
            return True
        except Exception as e:
            print(f"Error saving token: {e}")
            return False
