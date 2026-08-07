import os
import sys
import json
import urllib.request

def get_env(name, default=None, required=False):
    val = os.environ.get(name, default)
    if required and not val:
        print(f"Error: Missing required environment variable {name}")
        sys.exit(1)
    return val

def main():
    repo = get_env("GITHUB_REPOSITORY", required=True)
    pr_number = get_env("PR_NUMBER", required=True)
    token = get_env("GITHUB_TOKEN", required=True)
    
    max_lines = int(get_env("MAX_LINES", "500"))
    max_files = int(get_env("MAX_FILES", "10"))
    
    url = f"https://api.github.com/repos/{repo}/pulls/{pr_number}"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    req = urllib.request.Request(url, headers=headers)
    
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
            additions = data.get("additions", 0)
            deletions = data.get("deletions", 0)
            changed_files = data.get("changed_files", 0)
            pr_url = data.get("html_url", "")
            pr_author = data.get("user", {}).get("login", "Unknown")
    except Exception as e:
        print(f"Failed to fetch PR details: {e}")
        sys.exit(1)
        
    total_lines = additions + deletions
    
    print(f"Lines changed: {total_lines} (Max: {max_lines})")
    print(f"Files changed: {changed_files} (Max: {max_files})")
    
    if total_lines > max_lines or changed_files > max_files:
        print("🚨 PR exceeds size thresholds! Generating alert payload...")
        reason = []
        if total_lines > max_lines:
            reason.append(f"{total_lines} lines changed (limit {max_lines})")
        if changed_files > max_files:
            reason.append(f"{changed_files} files changed (limit {max_files})")
            
        payload = {
            "pr_number": pr_number,
            "pr_url": pr_url,
            "pr_author": pr_author,
            "reasons": " and ".join(reason)
        }
        
        # Write state to disk so downstream scripts can pick it up (Platform agnostic state passing)
        with open("alert_payload.json", "w") as f:
            json.dump(payload, f)
        print("Wrote alert_payload.json for downstream notifier scripts.")
    else:
        print("✅ PR size is within limits.")
        # Ensure we delete any stale payload file just in case
        if os.path.exists("alert_payload.json"):
            os.remove("alert_payload.json")

if __name__ == "__main__":
    main()
