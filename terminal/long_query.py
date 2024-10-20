import subprocess
import os
import tempfile
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
import server.setup

# Manually call the setup function from setup.py
setup_folder_path = 'buffer'  # Path where chat buffer is created
server.setup.setup_buffer(setup_folder_path)  # Makes chat.txt as a chatbot buffer

# Path to save Vim output
vim_output_file_path = os.path.join(setup_folder_path, 'chat_current_input.txt')

# Function to open Vim and return the input
def open_vim_and_get_input():
    # Create a temporary file for Vim to edit
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_filename = temp_file.name

    try:
        # Launch Vim and wait for the user to finish editing
        subprocess.run(['vim', temp_filename])

        # Read the content from the temporary file
        with open(temp_filename, 'r') as file:
            content = file.read()

    finally:
        # Cleanup the temporary file
        os.remove(temp_filename)

    return content