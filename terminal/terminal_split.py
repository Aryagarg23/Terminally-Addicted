import curses
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

# Main function for the curses interface
def main(stdscr):
    # Initial setup
    curses.curs_set(1)  # Show the cursor
    stdscr.nodelay(False)  # Blocking input for Enter key
    stdscr.clear()

    height, width = stdscr.getmaxyx()

    # Create split panes
    top_left = curses.newwin(height // 2, width // 2, 0, 0)
    bottom_left = curses.newwin(height // 2, width // 2, height // 2, 0)
    right_panel = curses.newwin(height, width // 2, 0, width // 2)  # Single long panel on the right

    # Text entry panel at the bottom
    text_entry_panel = curses.newwin(3, width, height - 3, 0)  # 3 rows high

    # Initial text
    placeholder_text = "Type '/' to enter command mode..."
    command_input = ""  # For storing the current command input
    typing_mode = False  # Flag for typing mode

    # Display the initial state of the panes
    top_left.addstr(1, 1, "Top Left Pane")
    bottom_left.addstr(1, 1, "Bottom Left Pane")
    right_panel.addstr(1, 1, "Bottom Right Pane")
    
    # Show placeholder text initially
    text_entry_panel.addstr(1, 1, f"> {placeholder_text}")  # Show placeholder text
    text_entry_panel.border()
    
    top_left.refresh()
    bottom_left.refresh()
    right_panel.refresh()
    text_entry_panel.refresh()

    while True:
        # Read input and only refresh when Enter is pressed
        key = stdscr.getch()

        # Exit on 'q'
        if key == ord('q'):
            break

        # Ignore mouse input
        if key == curses.KEY_MOUSE:
            continue

        # Check for starting command input
        if key == ord('/'):
            typing_mode = True
            command_input = ""  # Reset input when entering typing mode
            text_entry_panel.clear()
            text_entry_panel.border()
            text_entry_panel.refresh()  # Clear previous state

        # Handle command input if in typing mode
        if typing_mode:
            if key == curses.KEY_BACKSPACE or key == 127:  # Handle backspace
                command_input = command_input[:-1]
            elif key == curses.KEY_ENTER or key == 10:  # Enter key
                # If the command is "/chat"
                if command_input.startswith("/chat"):
                    # Handle /chat -v for Vim input
                    if command_input == "/chat -l":
                        # Close the curses interface temporarily and open Vim
                        curses.endwin()  # Close the curses window
                        vim_output = open_vim_and_get_input()  # Open Vim and get input
                        curses.doupdate()  # Restart the curses interface

                        # Save the Vim output to the text file
                        with open(vim_output_file_path, 'w+') as f:
                            f.write(vim_output)

                        # Put the Vim output into the top right panel
                        right_panel.clear()
                        right_panel.border()
                        right_panel.addstr(1, 1, f"User: ...\n{vim_output[-35:]}")  # Show the last part if long
                        right_panel.refresh()

                    elif command_input.startswith('/chat -s'):
                        right_panel.clear()
                        right_panel.border()
                        right_panel.addstr(1, 1, f"User: {command_input[9:]}")
                        right_panel.refresh()

                # Reset command input and show placeholder again
                command_input = ""
                typing_mode = False
                text_entry_panel.clear()
                text_entry_panel.border()
                text_entry_panel.addstr(1, 1, f"> {placeholder_text}")  # Show placeholder text
                text_entry_panel.refresh()
            else:
                # Add character to command input
                if chr(key).isprintable():  # Only allow printable characters
                    command_input += chr(key)

            # Display the current command input in the text entry panel
            text_entry_panel.clear()
            text_entry_panel.border()
            text_entry_panel.addstr(1, 1, f"> {command_input}")  # Show current input
            text_entry_panel.refresh()
        else:
            # Just refresh the text entry panel if not typing
            text_entry_panel.clear()
            text_entry_panel.border()
            text_entry_panel.addstr(1, 1, f"> {placeholder_text}")  # Show placeholder text
            text_entry_panel.refresh()

        # Update other panes, only when not typing
        if not typing_mode:
            top_left.clear()
            top_left.border()
            top_left.addstr(1, 1, "Top Left Pane")
            top_left.refresh()

            bottom_left.clear()
            bottom_left.border()
            bottom_left.addstr(1, 1, "Bottom Left Pane")
            bottom_left.refresh()

            # right_panel.clear()
            right_panel.border()
            # right_panel.addstr(1, 1, "Chat Pane")
            right_panel.refresh()

        # Disable scrolling
        stdscr.scrollok(False)
        stdscr.idlok(False)

curses.wrapper(main)
