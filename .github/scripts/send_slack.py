import os
import sys
import json
import urllib.request

def main():
    if not os.path.exists("alert_payload.json"):
        print("No alert payload found. Skipping Slack alert.")
        sys.exit(0)
        
    webhook_url = os.environ.get("SLACK_WEBHOOK_URL")
    if not webhook_url:
        print("Skipping Slack alert (no SLACK_WEBHOOK_URL configured).")
        sys.exit(0)
        
    with open("alert_payload.json", "r") as f:
        payload_data = json.load(f)
        
    slack_text = f"🚨 *Large PR Alert*\nPull Request <{payload_data['pr_url']}|#{payload_data['pr_number']}> by {payload_data['pr_author']} is exceptionally large.\n*Reason:* {payload_data['reasons']}.\nPlease consider breaking it down."
    
    data = json.dumps({"text": slack_text}).encode('utf-8')
    headers = {'Content-Type': 'application/json'}
    req = urllib.request.Request(webhook_url, data=data, headers=headers)
    try:
        with urllib.request.urlopen(req) as response:
            if response.status == 200:
                print("Slack alert sent successfully.")
    except Exception as e:
        print(f"Failed to send Slack alert: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
