# Pull Request Size Alert POC

## Overview
This repository contains a Proof of Concept (POC) for a platform-agnostic pipeline designed to monitor Pull Request (PR) sizes. When a PR exceeds predefined thresholds (modified lines or number of files), the pipeline automatically triggers notifications via Slack and/or SMTP Email.

The primary objective of this workflow is to enforce code review best practices by discouraging excessively large Pull Requests.

## Architecture
To prevent CI/CD vendor lock-in (e.g., being tied strictly to GitHub Actions), the core logic is implemented as **fully independent, standalone Python scripts**. 

These scripts rely entirely on the Python Standard Library (zero external dependencies) and can be executed as separate, distinct steps in any CI runner (Jenkins, GitLab CI, CircleCI, or GitHub Actions). State is passed between steps via a generated JSON payload file.

- **`scripts/check_pr_size.py`**: Interacts with the GitHub API, computes PR sizes against thresholds. If exceeded, it generates an `alert_payload.json` file.
- **`scripts/send_slack.py`**: If `alert_payload.json` exists, it reads the data and dispatches an alert via Slack Webhooks.
- **`scripts/send_email.py`**: If `alert_payload.json` exists, it reads the data and dispatches an alert via SMTP.
- **`.github/workflows/pr-size-alert.yml`**: A thin execution wrapper that runs the checking script, followed sequentially by the notification scripts.

## Threshold Conditions
The pipeline checks two specific conditions. An alert is triggered if **either** condition is met:
1. **Total Lines Changed** (Additions + Deletions) exceeds the defined limit (default: 500 lines).
2. **Total Files Changed** exceeds the defined limit (default: 10 files).

## Configuration Guide

The pipeline requires specific Environment Variables (injected via CI Secrets) to be configured prior to execution. 

### GitHub API Context (Required for check_pr_size.py)
- `GITHUB_TOKEN`: A token with read access to Pull Requests.
- `GITHUB_REPOSITORY`: The repository path (e.g., `owner/repo`).
- `PR_NUMBER`: The ID of the triggering Pull Request.

### Threshold Adjustments (Optional for check_pr_size.py)
- `MAX_LINES`: Maximum allowed line changes (Default: 500).
- `MAX_FILES`: Maximum allowed file changes (Default: 10).

### Slack Integration (Optional for send_slack.py)
1. Generate an **Incoming Webhook URL** in your target Slack workspace.
2. Inject the following environment variable:
   - `SLACK_WEBHOOK_URL`: Your designated Slack Webhook URL.

### SMTP Email Integration (Optional for send_email.py)
If email alerts are required, an active SMTP server is necessary.
1. Inject the following environment variables:
   - `SMTP_USERNAME`: The SMTP authentication username.
   - `SMTP_PASSWORD`: The SMTP authentication password.
   - `SMTP_SERVER`: (Optional) Defaults to `smtp.gmail.com`.
   - `SMTP_PORT`: (Optional) Defaults to `465`.
   - `ALERT_EMAIL_TO`: The target distribution list.

*Note: If a specific notification method is not required, simply omit those environment variables. The respective notification script will gracefully skip execution.*
