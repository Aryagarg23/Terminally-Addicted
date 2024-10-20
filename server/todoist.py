import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class TodoistAPI:
    def __init__(self):
        """Initialize the Todoist API with the base URL and headers."""
        self.api_token = os.getenv('TODOIST_API_TOKEN')
        self.base_url = 'https://api.todoist.com/rest/v2'
        self.headers = {
            'Authorization': f'Bearer {self.api_token}',
            'Content-Type': 'application/json'
        }

    def get_projects(self):
        """Fetch all projects from Todoist."""
        response = requests.get(f'{self.base_url}/projects', headers=self.headers)
        return self._handle_response(response)

    def create_task(self, content, due_string=None, priority=4):
        """Create a new task in Todoist."""
        data = {
            'content': content,
            'due_string': due_string,
            'priority': priority
        }
        response = requests.post(f'{self.base_url}/tasks', headers=self.headers, json=data)
        return self._handle_response(response)

    def close_task(self, task_id):
        """Close a task by its ID."""
        response = requests.post(f'{self.base_url}/tasks/{task_id}/close', headers=self.headers)
        return self._handle_response(response)

    def get_tasks(self):
        """Fetch all tasks from Todoist."""
        response = requests.get(f'{self.base_url}/tasks', headers=self.headers).json()
        strings = []
        for task in response:
            strings.append(f"{task['content']} due {task['due']['date']}")
        return strings

    def delete_task(self, task_id):
        """Delete a task by its ID."""
        response = requests.delete(f'{self.base_url}/tasks/{task_id}', headers=self.headers)
        return self._handle_response(response)

    def _handle_response(self, response):
        """Check if the response is successful; if not, raise an error."""
        if response.status_code == 204:
            return None  # Return None for 204 No Content response

        if response.status_code != 200:
            print(f"Error: {response.status_code} - {response.text}")
            response.raise_for_status()  # This will raise an HTTPError for bad responses
        
        try:
            return response.json()  # Attempt to parse JSON only if the response is OK
        except ValueError:
            print("Response content is not valid JSON:", response.text)
            return None  # Return None or handle it as needed

def main():
    """Main function to demonstrate the use of the Todoist API."""
    todoist = TodoistAPI()

    # Create a new task
    new_task = todoist.create_task('Buy groceries', 'tomorrow at 12:00')
    print("New Task:", new_task)

    # Fetch all tasks
    tasks = todoist.get_tasks()
    print("Tasks:", tasks)

if __name__ == '__main__':
    main()
