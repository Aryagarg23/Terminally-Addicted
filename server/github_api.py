import requests

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
    raise ValueError("Github token not found in the credentials file.")

# Optional headers for authentication
headers = {
    "Authorization": f"token {token}"
}

# Make the request
response = requests.get(url, headers=headers)

# Check the response
if response.status_code == 200:
    issues = response.json()
    for issue in issues:
        print(f"Issue #{issue['number']}: {issue['title']}")
else:
    print(f"Failed to retrieve issues: {response.status_code}")
