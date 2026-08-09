# Pull Request Size Alert POC

## Overview
This repository contains a Proof of Concept (POC) for a platform-agnostic pipeline designed to monitor Pull Request (PR) sizes. When a PR exceeds predefined thresholds (modified lines or number of files), the pipeline automatically triggers notifications via Slack, SMTP Email, and posts a visible comment directly on the PR timeline.

The primary objective of this workflow is to enforce code review best practices by discouraging excessively large Pull Requests.

## Architecture
To prevent CI/CD vendor lock-in (e.g., being tied strictly to GitHub Actions), the core logic is implemented as **fully independent, standalone Python scripts**. 

These scripts rely entirely on the Python Standard Library (zero external dependencies) and can be executed as separate, distinct steps in any CI runner (Jenkins, GitLab CI, CircleCI, or GitHub Actions). State is passed between steps via a generated JSON payload file.

### Components
- **`.github/scripts/check_pr_size.py`**: Interacts with the GitHub API via the `gh` CLI, computes PR sizes against thresholds, and automatically ignores files based on the `.prignorecheck` configuration. If limits are exceeded, it generates an `alert_payload.json` file and automatically posts a warning comment to the PR.
- **`.github/scripts/send_slack.py`**: If `alert_payload.json` exists, it reads the data and dispatches an alert via Slack Webhooks.
- **`.github/scripts/send_email.py`**: If `alert_payload.json` exists, it reads the data and dispatches an alert via SMTP.
- **`.github/workflows/pr-size-alert.yml`**: A thin execution wrapper that runs the checking script, followed sequentially by the notification scripts. Finally, it checks for the existence of `alert_payload.json` to safely fail the job and turn the PR check Red ❌.

## How to Test the POC
This repository comes with a dummy Python application in the `src/` directory to help you test the alerts realistically.
1. Create a new branch (e.g., `git checkout -b test-large-pr`).
2. Make extensive changes to `src/calculator.py` or create new files to exceed the defined thresholds.
3. Commit and push your changes.
4. Open a Pull Request against the `main` branch. 
5. The `PR Size Alert` check will automatically run, post a comment, and trigger Slack/Email alerts.

## ⚙️ The `.prignorecheck` Feature
You can define a `.prignorecheck` file in the root of the repository to specify directories or files that should **not** count towards the PR size limits (like tests or documentation).

- The file works similarly to `.gitignore`.
- Simply list the prefix of the file or folder (e.g., `tests/` or `docs/README.md`).
- *Note: By default, the `.github/` folder is hardcoded to be ignored.*

## Configuration Guide

The pipeline requires specific Environment Variables (injected via CI Secrets) to be configured prior to execution. 

### GitHub API Context (Required for check_pr_size.py)
- `GITHUB_TOKEN`: A token with read/write access to Pull Requests (for fetching size and posting comments).
- `GITHUB_REPOSITORY`: The repository path (e.g., `owner/repo`).
- `PR_NUMBER`: The ID of the triggering Pull Request.

### Threshold Adjustments (Optional for check_pr_size.py)
- `MAX_LINES`: Maximum allowed line changes (Default: 500).
- `MAX_FILES`: Maximum allowed file changes (Default: 10).

### Slack Integration (Optional for send_slack.py)
1. Generate an **Incoming Webhook URL** in your target Slack workspace.
2. Add a **Repository Secret** named `SLACK_WEBHOOK_URL`.

### SMTP Email Integration (Optional for send_email.py)
If email alerts are required, an active SMTP server is necessary.
1. Inject the following environment variables:
   - `SMTP_USERNAME`: The SMTP authentication username.
   - `SMTP_PASSWORD`: The SMTP authentication password.
   - `SMTP_SERVER`: (Optional) Defaults to `smtp.gmail.com`.
   - `SMTP_PORT`: (Optional) Defaults to `465`.
   - `ALERT_EMAIL_TO`: The target distribution list.

*Note: If a specific notification method is not required, simply omit those environment variables (or leave the Secrets blank). The respective notification script will gracefully skip execution without crashing.*
