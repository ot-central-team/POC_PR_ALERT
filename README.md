# CI/CD PR Size Alert POC 🚀

Welcome to the Pull Request Size Alert POC! This repository contains a production-ready, highly modular GitHub Actions setup designed to monitor the size of incoming Pull Requests and send alerts (via Slack or Email) if a PR exceeds a specified line-change threshold.

This encourages developers to keep Pull Requests small, making them easier to review, less prone to bugs, and faster to merge.

## Architecture

We have modularized the pipeline using **GitHub Composite Actions**. This means the logic is decoupled and can be reused across any repository in the organization.

- **`.github/workflows/pr-size-alert.yml`**: The main orchestrator workflow. It listens for PR events and calls the composite actions.
- **`.github/actions/pr-size-calculator`**: Uses the native GitHub CLI (`gh`) to securely fetch the exact number of additions and deletions.
- **`.github/actions/pr-alert-on-slack`**: A dedicated module for sending Slack notifications using official Slack actions.
- **`.github/actions/pr-alert-on-mail`**: A dedicated module for sending SMTP Email notifications.

## How it Works

1. A developer opens or synchronizes a Pull Request.
2. The `pr-size-alert.yml` workflow triggers.
3. The **Calculator Action** computes the total lines changed (additions + deletions).
4. If `Total Changes > THRESHOLD` (default: 500 lines), it flags `exceeds_threshold=true`.
5. The **Slack / Email Actions** check this flag. If `true`, they dispatch a notification contawining the PR link, author, and size.

## Setup & Configuration (For Junior Devs)

To make this work in your repository, you need to configure a few GitHub Secrets. 

Go to **Settings > Secrets and variables > Actions > New repository secret**.

### 1. Slack Setup (Recommended)
Slack is the easiest and most reliable method.
1. In your Slack Workspace, create a new **Incoming Webhook** for the channel you want alerts in.
2. Add the webhook URL to your GitHub Secrets:
   - **Name**: `SLACK_WEBHOOK_URL`
   - **Value**: `https://hooks.slack.com/services/YOUR/WEBHOOK/URL`

### 2. Email Setup (Optional)
If you prefer email alerts, you need an SMTP server (e.g., Gmail, Amazon SES, SendGrid).
1. Add the following to your GitHub Secrets:
   - **Name**: `SMTP_USERNAME` (Your SMTP email address)
   - **Name**: `SMTP_PASSWORD` (Your SMTP App Password)
2. In `.github/workflows/pr-size-alert.yml`, update the `alert_email_to` field to your team's email address.

> **Pro Tip:** If you ONLY want to use Slack, you can safely delete or comment out the `Send Email Alert` step in `.github/workflows/pr-size-alert.yml`. If you leave it in without adding the SMTP secrets, the action will throw an error expecting those inputs.

## 🛠️ Customizing the Threshold

You can easily change the PR size limit. Open `.github/workflows/pr-size-alert.yml` and look for the `env` block at the top of the job:

```yaml
    env:
      # Set your line change threshold here
      THRESHOLD: 500 
```
Change `500` to whatever fits your team's standards!

## Production Readiness Check
- **Secure**: Uses `GITHUB_TOKEN` securely with the `gh` CLI without exposing it.
- **Modular**: Logic is abstracted into reusable actions.
- **Standardized**: Uses verified community actions (`slackapi/slack-github-action` & `dawidd6/action-send-mail`).
- **Resilient**: Triggers on `opened`, `synchronize`, and `reopened` to catch all PR activity.
