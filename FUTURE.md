# Future Features

Based on the current architecture of `ghman`, here are the top key features we could could consider adding to enhance its utility:

## 1. Repository Management & Lifecycle
*   **Archiving**: A `ghman archive [repo]` command to mark repositories as archived when they are no longer active but should be preserved.
*   **Visibility Toggle**: Commands like `ghman private [repo]` or `ghman public [repo]` to quickly change repository visibility without visiting the web UI.

## 2. Enhanced "Add" Workflow
*   **Template Support**: Add a `--template [user/repo]` flag to the `add` command to initialize your new repository from an existing GitHub template.
*   **Auto-ignore/License**: Integrate options to automatically generate a basic `.gitignore` (based on language) or a `LICENSE` file during the `add` process.
*   **Custom Remote Names**: Allow users to specify a remote name other than `origin` (e.g., `--remote upstream`).

## 3. Repository Discovery & Insights
*   **Interactive TUI**: Implement an interactive list (using a library like `rich` or `questionary`) that allows you to scroll through repositories and see details like stars, forks, and open issues.
*   **`ghman info [repo]`**: Display detailed information about a specific repository, including its clone URL, creation date, and last push time.
*   **Organization Support**: Add a `--org [name]` flag to `list` and `add` to manage repositories within a specific GitHub Organization rather than just your personal account.

## 4. Local Workspace Sync
*   **`ghman sync`**: A command that scans your local directories to check if they have corresponding GitHub remotes and highlights any "untracked" local projects.
*   **Bulk Clone**: A command to clone all (or a filtered subset) of your repositories to a local machine in one go—useful for setting up a new workstation.

## 5. Automation & Notifications
*   **Issue/PR Listing**: Briefly list open Pull Requests or Issues for your repositories to get a high-level "pulse" of your projects.
*   **CI/CD Status**: Integration with GitHub Actions to show the pass/fail status of the latest workflow run for your repositories directly in the `list` output.

## 6. Security & Infrastructure
*   **Multi-Profile Support**: Support for multiple GitHub accounts (e.g., `work` and `personal`) with easy switching between them using `ghman auth switch`.
*   **Token Scoping Check**: A small utility to verify if the currently active token has the necessary permissions for the requested action, providing more helpful error messages.
