#!/usr/bin/env python3
import argparse
import os
import sys
import subprocess
from client import GitHubClient

def run_command(command, cwd=None):
    """Runs a shell command and returns the output."""
    try:
        result = subprocess.run(
            command,
            cwd=cwd,
            check=True,
            capture_output=True,
            text=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error running command {' '.join(command)}: {e.stderr}")
        return None

def handle_list(args):
    client = GitHubClient()
    print(f"Fetching repositories for authenticated user...")
    repos = client.list_repositories()
    if not repos:
        print("No repositories found or error occurred.")
        return

    print("\nExisting Repositories:")
    for repo in sorted(repos):
        print(f"- {repo}")

def handle_auth(args):
    token = args.token
    if not token:
        import getpass
        token = getpass.getpass("Enter your GitHub Personal Access Token: ")
    
    if GitHubClient.save_token(token):
        print("Successfully saved token to ~/.ghman/config.json")
        print("Permissions set to 600 (owner only readable).")
    else:
        print("Failed to save token.")
        sys.exit(1)

def handle_add(args):
    repo_name = args.name
    if not repo_name:
        repo_name = os.path.basename(os.getcwd())
    
    # 1. Ensure local Git repository exists
    if not os.path.exists(".git"):
        print("Error: Current directory is not a Git repository.")
        print("Please run 'git init' and add some files first.")
        sys.exit(1)

    client = GitHubClient()

    # 2. Check if repository exists on GitHub
    print(f"Checking if repository '{repo_name}' already exists on GitHub...")
    repo = client.get_repository(repo_name)
    if repo:
        print(f"Repository '{repo_name}' already exists on GitHub. Using existing.")
    else:
        # 3. Create the repository on GitHub
        print(f"Creating repository '{repo_name}' on GitHub...")
        repo = client.create_repository(repo_name, private=args.private)
        if not repo:
            print(f"Error: Failed to create repository '{repo_name}'.")
            sys.exit(1)
        print(f"Successfully created: {repo.html_url}")

    # 4. Handle local Git setup
    print("Setting up local repository...")

    # Add remote
    print(f"Adding remote 'origin' to {repo.ssh_url}...")
    # Remove existing origin if it exists
    try:
        subprocess.run(
            ["git", "remote", "remove", "origin"],
            capture_output=True
        )
    except:
        pass
    
    run_command(["git", "remote", "add", "origin", repo.ssh_url])

    # Initial commit and push if there are files
    if os.listdir('.'):
        print("Committing and pushing local files...")
        run_command(["git", "add", "."])
        # Check if there's anything to commit
        status = run_command(["git", "status", "--short"])
        if status:
            run_command(["git", "commit", "-m", "Initial commit from ghman"])
        
        # Determine current branch name
        branch = run_command(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"]
        ) or "main"
        if branch == "HEAD": # empty repo
            run_command(["git", "branch", "-M", "main"])
            branch = "main"
            
        print(f"Pushing to origin {branch}...")
        run_command(["git", "push", "-u", "origin", branch])

    print("\nDone! Your repository is now on GitHub.")

def handle_delete(args):
    repo_name = args.name
    client = GitHubClient()
    
    # Confirmation prompt
    print(f"WARNING: You are about to delete repository '{repo_name}' from GitHub.")
    print("This action is irreversible.")
    confirm = input(f"Type '{repo_name}' to confirm deletion: ")
    
    if confirm == repo_name:
        print(f"Deleting repository '{repo_name}'...")
        if client.delete_repository(repo_name):
            print(f"Successfully deleted repository '{repo_name}'.")
        else:
            print(f"Failed to delete repository '{repo_name}'.")
    else:
        print("Deletion cancelled. Confirmation name did not match.")

def main():
    parser = argparse.ArgumentParser(
        description="ghman: A simple GitHub repository manager."
    )
    subparsers = parser.add_subparsers(
        dest="command", help="Available commands"
    )

    # List command
    subparsers.add_parser("list", help="List your GitHub repositories")

    # Add command
    add_parser = subparsers.add_parser(
        "add", help="Add the current local repository to GitHub"
    )
    add_parser.add_argument(
        "name", nargs="?", help="Name of the repository to create on GitHub (defaults to directory name)"
    )
    add_parser.add_argument(
        "--public", action="store_false", dest="private",
        help="Make the repository public (default is private)"
    )
    add_parser.set_defaults(private=True)

    # Delete command
    delete_parser = subparsers.add_parser(
        "delete", help="Delete a repository from GitHub"
    )
    delete_parser.add_argument(
        "name", help="Name of the repository to delete"
    )

    # Auth command
    auth_parser = subparsers.add_parser(
        "auth", help="Configure GitHub authentication"
    )
    auth_parser.add_argument(
        "--token", help="GitHub Personal Access Token (PAT)"
    )

    args = parser.parse_args()

    if args.command == "list":
        handle_list(args)
    elif args.command == "add":
        handle_add(args)
    elif args.command == "auth":
        handle_auth(args)
    elif args.command == "delete":
        handle_delete(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
