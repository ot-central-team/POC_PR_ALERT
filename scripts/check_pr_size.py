import os
import sys
import json
import subprocess

def get_env(name, default=None, required=False):
    val = os.environ.get(name, default)
    if required and not val:
        print(f"Error: Missing required environment variable {name}")
        sys.exit(1)
    return val

def main():
    repo = get_env("GITHUB_REPOSITORY", required=True)
    pr_number = get_env("PR_NUMBER", required=True)
    
    max_lines = int(get_env("MAX_LINES", "500"))
    max_files = int(get_env("MAX_FILES", "10"))
    
    try:
        cmd = ["gh", "pr", "view", pr_number, "--repo", repo, "--json", "url,author,files"]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        data = json.loads(result.stdout)
        pr_url = data.get("url", "")
        pr_author = data.get("author", {}).get("login", "Unknown")
        files_data = data.get("files", [])
    except subprocess.CalledProcessError as e:
        print(f"Failed to fetch PR details using gh CLI: {e.stderr}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)
        
    ignore_prefixes = ["scripts/", ".github/"]
    if os.path.exists(".prignorecheck"):
        with open(".prignorecheck", "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    ignore_prefixes.append(line)
                    
    total_lines = 0
    changed_files = 0
    
    for file_obj in files_data:
        filename = file_obj.get("path", "")
        if any(filename.startswith(prefix) for prefix in ignore_prefixes):
            continue
            
        additions = file_obj.get("additions", 0)
        deletions = file_obj.get("deletions", 0)
        total_lines += (additions + deletions)
        changed_files += 1
            
    print(f"Filtered Lines changed: {total_lines} (Max: {max_lines})")
    print(f"Filtered Files changed: {changed_files} (Max: {max_files})")
    
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
