import os

def setup_buffer(folder_path):
    """
    Sets up the buffer by creating the folder (if not exists)
    and creating (or overwriting) a 'chat.txt' file within it.
    
    Args:
        folder_path (str): Path to the folder where 'chat.txt' will be created.
    """
    # Check if the folder exists, if not, create it
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"Folder '{folder_path}' created.")
    else:
        print(f"Folder '{folder_path}' already exists.")

    # Define the file path for the "chat.txt"
    file_path = os.path.join(folder_path, 'chat.txt')

    # Create (or overwrite) the "chat.txt" file
    with open(file_path, 'w') as file:
        file.write("This is the chat log.\n")

    print(f"'chat_current_input.txt' has been created in {folder_path}")
        # Define the file path for the "chat.txt"
    file_path = os.path.join(folder_path, 'chat_current_input.txt')

    # Create (or overwrite) the "chat.txt" file
    with open(file_path, 'w') as file:
        file.write("This is the chat log.\n")

    print(f"'chat_current_input.txt' has been created in {folder_path}")

# Call the setup function
if __name__ == "__main__":
    buffer_folder = 'buffer'  # Replace with the actual path to the "buffer" folder
    setup_buffer(buffer_folder)
