# Context: Pull Request Size Alert POC (`poc_cipr`)

## Project Overview
This repository (`poc_cipr`) contains a Proof of Concept (POC) for a platform-agnostic CI/CD pipeline that monitors the size of Pull Requests. When a PR exceeds predefined thresholds for either modified lines or number of files, it triggers notifications to Slack and/or Email.

The goal is to encourage smaller, more reviewable pull requests.

## Architecture
The logic is intentionally decoupled from CI/CD vendor-specific features (like GitHub Actions) and relies on independent Python scripts with no external dependencies (only the Python Standard Library). This allows the scripts to be run as steps in any CI environment (Jenkins, GitLab CI, CircleCI, etc.).

State is passed between steps using a generated JSON file named `alert_payload.json`.

### Components
1. **`.github/workflows/pr-size-alert.yml`**
   - The execution wrapper for GitHub Actions. It sets up Python, passes required environment variables, and sequentially runs the Python scripts.
2. **`scripts/check_pr_size.py`**
   - Interacts with the GitHub API to fetch PR size data.
   - Compares data against thresholds (`MAX_LINES` default 500, `MAX_FILES` default 10).
   - If the PR is too large, it generates `alert_payload.json` containing the PR details and the reason for the alert.
3. **`scripts/send_slack.py`**
   - Checks for the existence of `alert_payload.json`.
   - If found, formats the data and sends a message using a Slack Incoming Webhook (`SLACK_WEBHOOK_URL`).
4. **`scripts/send_email.py`**
   - Checks for the existence of `alert_payload.json`.
   - If found, formats an email and sends it via SMTP using credentials provided via environment variables.

## Environment Variables / Secrets Used
- **GitHub**: `GITHUB_TOKEN`, `GITHUB_REPOSITORY`, `PR_NUMBER`
- **Thresholds**: `MAX_LINES`, `MAX_FILES`
- **Slack**: `SLACK_WEBHOOK_URL`
- **Email**: `SMTP_USERNAME`, `SMTP_PASSWORD`, `SMTP_SERVER`, `SMTP_PORT`, `ALERT_EMAIL_TO`
