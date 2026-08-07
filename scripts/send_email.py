import os
import sys
import json
import smtplib
from email.message import EmailMessage

def main():
    if not os.path.exists("alert_payload.json"):
        print("No alert payload found. Skipping Email alert.")
        sys.exit(0)
        
    smtp_user = os.environ.get("SMTP_USERNAME")
    smtp_pass = os.environ.get("SMTP_PASSWORD")
    alert_to = os.environ.get("ALERT_EMAIL_TO")
    
    if not (smtp_user and smtp_pass and alert_to):
        print("Skipping Email alert (missing SMTP credentials or target email).")
        sys.exit(0)
        
    smtp_server = os.environ.get("SMTP_SERVER", "smtp.gmail.com")
    smtp_port = int(os.environ.get("SMTP_PORT", "465"))
    alert_from = os.environ.get("ALERT_EMAIL_FROM", "CI/CD Pipeline <actions@example.com>")
    
    with open("alert_payload.json", "r") as f:
        payload_data = json.load(f)
        
    email_subject = f"🚨 Large PR Alert: PR #{payload_data['pr_number']}"
    email_body = f"Pull Request #{payload_data['pr_number']} by {payload_data['pr_author']} is exceptionally large.\n\nReason: {payload_data['reasons']}.\n\nPlease review: {payload_data['pr_url']}"
    
    msg = EmailMessage()
    msg.set_content(email_body)
    msg['Subject'] = email_subject
    msg['From'] = alert_from
    msg['To'] = alert_to

    try:
        server_obj = smtplib.SMTP_SSL(smtp_server, smtp_port)
        server_obj.login(smtp_user, smtp_pass)
        server_obj.send_message(msg)
        server_obj.quit()
        print("Email alert sent successfully.")
    except Exception as e:
        print(f"Failed to send Email alert: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
