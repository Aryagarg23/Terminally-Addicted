import requests
import os
from dotenv import load_dotenv




class GitHubIssueManager:
    def __init__(self, owner = "Aryagarg23",repo = "Terminally-Addicted"):
        self.owner = owner
        self.repo = repo
        load_dotenv()
        self.token = os.getenv('GITHUB_TOKEN', '')
        self.base_url = f"https://api.github.com/repos/{self.owner}/{self.repo}/issues"
        self.headers = {
            "Authorization": f"token {self.token}"
        }

    def set_owner_repo(self, owner, repo):
        self.owner = owner
        self.repo = repo
        self.base_url = f"https://api.github.com/repos/{self.owner}/{self.repo}/issues"
        
    def create_issue(self, title, body=None, labels=None):
        issue_data = {
            "title": title,
            "body": body,
            "labels": labels if labels else []
        }
        
        response = requests.post(self.base_url, json=issue_data, headers=self.headers)

        if response.status_code == 201:
            return f"Issue created: #{response.json()['number']}"
        else:
            return f"Failed to create issue: {response.status_code}, {response.text}"

    def close_issue(self, issue_number):
        url = f"{self.base_url}/{issue_number}"
        
        issue_data = {
            "state": "closed"
        }

        response = requests.patch(url, json=issue_data, headers=self.headers)

        if response.status_code == 200:
            return f"Issue #{issue_number} closed successfully."
        else:
            return f"Failed to close issue #{issue_number}: {response.status_code}, {response.text}"

    def comment_on_issue(self, issue_number, comment):
        url = f"{self.base_url}/{issue_number}/comments"
        
        comment_data = {
            "body": comment
        }

        response = requests.post(url, json=comment_data, headers=self.headers)

        if response.status_code == 201:
            return f"Comment added to issue #{issue_number}."
        else:
            return f"Failed to add comment to issue #{issue_number}: {response.status_code}, {response.text}"

    def list_issues(self, state='open'):
        url = f"{self.base_url}?state={state}"

        response = requests.get(url, headers=self.headers)

        if response.status_code == 200:
            issues = response.json()
            if not issues:
                return f"No {state} issues found."
            result = []
            for issue in issues:
                result.append(f"Issue #{issue['number']}: {issue['title']} (State: {issue['state']})")
            return "\n ".join(result)
        else:
            return f"Failed to retrieve {state} issues: {response.status_code}, {response.text}"

    def update_issue(self, issue_number, new_title=None, new_body=None):
        url = f"{self.base_url}/{issue_number}"

        issue_data = {}
        if new_title:
            issue_data["title"] = new_title
        if new_body:
            issue_data["body"] = new_body

        response = requests.patch(url, json=issue_data, headers=self.headers)

        if response.status_code == 200:
            return f"Issue #{issue_number} updated successfully."
        else:
            return f"Failed to update issue #{issue_number}: {response.status_code}, {response.text}"

    def search_issues_by_label(self, label):
        url = f"{self.base_url}?labels={label}"

        response = requests.get(url, headers=self.headers)

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

    def test_github_issue_functions(self):
        try:
            # Step 1: Create an issue
            issue_title = "Test Issue for GitHub API"
            issue_body = "This issue was created for testing purposes."
            issue_labels = ["bug"]

            print("Creating an issue...")
            create_response = self.create_issue(issue_title, body=issue_body, labels=issue_labels)
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
            comment_response = self.comment_on_issue(issue_number, comment)
            print(comment_response)

            # Step 3: Update the issue with a new title and body
            new_title = "Updated Test Issue Title"
            new_body = "This is the updated body of the test issue."
            print(f"Updating issue #{issue_number}...")
            update_response = self.update_issue(issue_number, new_title=new_title, new_body=new_body)
            print(update_response)

            # Step 4: List all open issues
            print("Listing all open issues...")
            open_issues = self.list_issues(state='open')
            print(open_issues)

            # Step 5: Search issues by label (optional)
            if issue_labels:
                search_label = issue_labels[0]
                print(f"Searching issues by label '{search_label}'...")
                search_response = self.search_issues_by_label(search_label)
                print(search_response)

            # Step 6: Close the issue
            print(f"Closing issue #{issue_number}...")
            close_response = self.close_issue(issue_number)
            print(close_response)

            # Step 7: List all closed issues
            print("Listing all closed issues...")
            closed_issues = self.list_issues(state='closed')
            print(closed_issues)

        except Exception as e:
            print(f"An error occurred during testing: {e}")
