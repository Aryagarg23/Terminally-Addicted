import requests
import argparse

# Replace these with your own values
owner = "Aryagarg23"
repo = "Terminally-Addicted"
url = f"https://api.github.com/repos/{owner}/{repo}/issues"

# Read the access token from the file
with open('/Users/kaaustaaubshankar/Documents/Coding/Terminally-Addicted/server/spotify_credentials.txt', 'r') as file:
    lines = file.readlines()
    token = None
    for line in lines:
        if line.startswith("GITHUB_TOKEN="):
            token = line.split("GITHUB_TOKEN=")[1].strip()
            break

if not token:
    raise ValueError("GitHub token not found in the credentials file.")

# Optional headers for authentication
headers = {
    "Authorization": f"token {token}"
}

# Function to create an issue
def create_issue(title, body=None, labels=None):
    issue_data = {
        "title": title,
        "body": body,
        "labels": labels if labels else []
    }

    response = requests.post(url, json=issue_data, headers=headers)

    if response.status_code == 201:
        return f"Issue created: #{response.json()['number']}"
    else:
        return f"Failed to create issue: {response.status_code}, {response.text}"

# Function to close an issue
def close_issue(issue_number):
    url = f"https://api.github.com/repos/{owner}/{repo}/issues/{issue_number}"
    
    issue_data = {
        "state": "closed"
    }

    response = requests.patch(url, json=issue_data, headers=headers)

    if response.status_code == 200:
        return f"Issue #{issue_number} closed successfully."
    else:
        return f"Failed to close issue #{issue_number}: {response.status_code}, {response.text}"

# Function to add a comment to an issue
def comment_on_issue(issue_number, comment):
    url = f"https://api.github.com/repos/{owner}/{repo}/issues/{issue_number}/comments"
    
    comment_data = {
        "body": comment
    }

    response = requests.post(url, json=comment_data, headers=headers)

    if response.status_code == 201:
        return f"Comment added to issue #{issue_number}."
    else:
        return f"Failed to add comment to issue #{issue_number}: {response.status_code}, {response.text}"

# Function to list all issues
def list_issues(state='open'):
    url = f"https://api.github.com/repos/{owner}/{repo}/issues?state={state}"

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        issues = response.json()
        if not issues:
            return f"No {state} issues found."
        result = []
        for issue in issues:
            result.append(f"Issue #{issue['number']}: {issue['title']} (State: {issue['state']})")
        return "\n".join(result)
    else:
        return f"Failed to retrieve {state} issues: {response.status_code}, {response.text}"

# Function to update an issue
def update_issue(issue_number, new_title=None, new_body=None):
    url = f"https://api.github.com/repos/{owner}/{repo}/issues/{issue_number}"

    issue_data = {}
    if new_title:
        issue_data["title"] = new_title
    if new_body:
        issue_data["body"] = new_body

    response = requests.patch(url, json=issue_data, headers=headers)

    if response.status_code == 200:
        return f"Issue #{issue_number} updated successfully."
    else:
        return f"Failed to update issue #{issue_number}: {response.status_code}, {response.text}"

# Function to search issues by label
def search_issues_by_label(label):
    url = f"https://api.github.com/repos/{owner}/{repo}/issues?labels={label}"

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        issues = response.json()
        if not issues:
            return f"No issues found with label: {label}."
        result = []
        for issue in issues:
            result.append(f"Issue #{issue['number']}: {issue['title']}")
        return "\n".join(result)
    else:
        return f"Failed to search issues: {response.status_code}, {response.text}"

def test_github_issue_functions():
    try:
        # Step 1: Create an issue
        issue_title = "Test Issue for GitHub API"
        issue_body = "This issue was created for testing purposes."
        issue_labels = ["bug"]  # Example label, you can change or remove this

        print("Creating an issue...")
        create_response = create_issue(issue_title, body=issue_body, labels=issue_labels)
        print(create_response)

        # Extract the issue number from the response
        issue_number = None
        if "Issue created" in create_response:
            issue_number = int(create_response.split("#")[1].split()[0])

        if not issue_number:
            print("Error: Issue number not found.")
            return

        # Step 2: Add a comment to the created issue
        comment = "This is a test comment added to the issue."
        print(f"Adding comment to issue #{issue_number}...")
        comment_response = comment_on_issue(issue_number, comment)
        print(comment_response)

        # Step 3: Update the issue with a new title and body
        new_title = "Updated Test Issue Title"
        new_body = "This is the updated body of the test issue."
        print(f"Updating issue #{issue_number}...")
        update_response = update_issue(issue_number, new_title=new_title, new_body=new_body)
        print(update_response)

        # Step 4: List all open issues
        print("Listing all open issues...")
        open_issues = list_issues(state='open')
        print(open_issues)

        # Step 5: Search issues by label (optional)
        if issue_labels:
            search_label = issue_labels[0]
            print(f"Searching issues by label '{search_label}'...")
            search_response = search_issues_by_label(search_label)
            print(search_response)

        # Step 6: Close the issue
        print(f"Closing issue #{issue_number}...")
        close_response = close_issue(issue_number)
        print(close_response)

        # Step 7: List all closed issues
        print("Listing all closed issues...")
        closed_issues = list_issues(state='closed')
        print(closed_issues)

    except Exception as e:
        print(f"An error occurred during testing: {e}")


# Call the test function
test_github_issue_functions()

