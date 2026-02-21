# ghman

A simple GitHub repository manager CLI utility designed to streamline your workflow. `ghman` saves you time by automating the creation and linking of local projects to GitHub in a single command, and provides a quick way to list and track all your existing repositories directly from the terminal.

## Prerequisites

- Python 3.6+
- A GitHub Personal Access Token (PAT) with `repo` scope.

## Installation

### One-Step Installation (Recommended)

Run the included installation script to set up dependencies and permissions automatically:

```bash
./install.sh
```

### Manual Installation

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Make the script executable:
   ```bash
   chmod +x ghman.py
   ```

## Uninstallation

To remove `ghman`'s configuration and symlinks, run:

```bash
./uninstall.sh
```

This will:
- Remove the symlink from `/usr/local/bin/ghman` (if present).
- Optionally remove the configuration directory and saved token (`~/.ghman`).

## Configuration

### Obtain a GitHub Personal Access Token (PAT)

To use `ghman`, you need a GitHub PAT with `repo` scope:

1.  Log in to your [GitHub account](https://github.com).
2.  Navigate to **Settings** > **Developer settings** > **Personal access tokens** > **Tokens (classic)**.
3.  Click **Generate new token** (select **Generate new token (classic)**).
4.  Give it a descriptive name (e.g., "ghman CLI").
5.  Select the **`repo`** scope (this allows creating and managing repositories).
6.  Click **Generate token** at the bottom.
7.  **Copy the token immediately**—you won't be able to see it again!

### Set Environment Variable

Set your PAT as an environment variable in your terminal session:

```bash
export GITHUB_TOKEN=your_token_here
```

### Persistent Configuration (Recommended)

For a safer and more permanent way to store your token, use the `auth` command. This will save your token to `~/.ghman/config.json` and set the file permissions to `600` (readable only by you):

```bash
./ghman auth
```
You will be prompted to enter your token securely (input will be hidden). Alternatively, you can pass it directly:
```bash
./ghman auth --token your_token_here
```

> [!TIP]
> `ghman` will check the `GITHUB_TOKEN` environment variable first. If not found, it will look for the saved token in `~/.ghman/config.json`.

## Usage

### List Repositories
List all repositories on your GitHub account:
```bash
./ghman list
```

### Add Local Repository
Add the current directory as a new or existing repository on GitHub:
```bash
./ghman add [repo-name]
```

Options:
- `[repo-name]`: Optional name for the GitHub repository (defaults to the current directory name).
- `--public`: Create a public repository (default is private).

## Features
- Checks if a repository already exists on GitHub and link to it if so.
- Requires an existing local Git repository.
- Adds the correct remote and pushes local code.
## License

This project is licensed under the BSD 3-Clause License - see the [LICENSE](file:///Users/vlad/.gemini/antigravity/scratch/ghman/LICENSE) file for details.
