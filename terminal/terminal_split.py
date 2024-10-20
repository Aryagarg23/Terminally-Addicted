import curses
import subprocess
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from long_query import open_vim_and_get_input
from server.spotify_api import display_current_playback

# Main function for the curses interface
def main(stdscr):
    # Initial setup
    curses.curs_set(1)  # Show the cursor
    stdscr.nodelay(False)  # Blocking input for Enter key
    stdscr.clear()

    height, width = stdscr.getmaxyx()

    curses.start_color()  # Start color functionality
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)  # User output color (green text)
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)  # Placeholder color (yellow text)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)   # Border color (white text)

    # Create split panes
    top_left = curses.newwin(height // 2, width // 2, 0, 0)
    bottom_left = curses.newwin(height // 2 - 2, width // 2, height // 2, 0)
    right_panel = curses.newwin(height - 3, width // 2, 0, width // 2)  # Single long panel on the right

    # Text entry panel at the bottom
    text_entry_panel = curses.newwin(3, width, height - 3, 0)  # 3 rows high

    # Initial text
    placeholder_text = display_current_playback()
    command_input = ""  # For storing the current command input
    typing_mode = False  # Flag for typing mode

    # List to store user outputs
    user_outputs = []
    current_page = 0  # Track the current page
    page_size = 10  # Number of outputs per page

    # Display the initial state of the panes
    top_left.addstr(1, 1, "Top Left Pane", curses.color_pair(3))  # Border color
    bottom_left.addstr(1, 1, "Bottom Left Pane", curses.color_pair(3))  # Border color
    right_panel.addstr(1, 1, "Right Panel (User Outputs)", curses.color_pair(3))  # Border color

    # Show placeholder text initially
    text_entry_panel.addstr(1, 1, f"> {placeholder_text}", curses.color_pair(2))  # Show placeholder text in yellow
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
                        with open('../buffer/chat_current_input.txt', 'w+') as f:
                            f.write(vim_output)

                        # Add Vim output to user outputs
                        user_outputs.append(f"User: {vim_output.strip()}")  # Append output to the list

                        # Display outputs for the current page
                        right_panel.clear()
                        right_panel.border()
                        start_index = current_page * page_size
                        end_index = start_index + page_size
                        for i, output in enumerate(user_outputs[start_index:end_index], start=2):  # Start at row 2 to leave space for the border
                            right_panel.addstr(i, 1, output, curses.color_pair(1))  # Show all user outputs in green
                        right_panel.refresh()

                    elif command_input.startswith('/chat -s'):
                        user_outputs.append(f"User: {command_input[9:]}")  # Append output to the list

                        # Display outputs for the current page
                        right_panel.clear()
                        right_panel.border()
                        start_index = current_page * page_size
                        end_index = start_index + page_size
                        for i, output in enumerate(user_outputs[start_index:end_index], start=2):  # Start at row 2 to leave space for the border
                            right_panel.addstr(i, 1, output, curses.color_pair(1))  # Show all user outputs in green
                        right_panel.refresh()

                # Reset command input and show placeholder again
                command_input = ""
                typing_mode = False
                text_entry_panel.clear()
                text_entry_panel.border()
                text_entry_panel.addstr(1, 1, f"> {placeholder_text}", curses.color_pair(2))  # Show placeholder text
                text_entry_panel.refresh()

            # Handle pagination commands
            elif command_input.startswith("/p"):
                if command_input[-1] == 'n':  # Next page
                    if (current_page + 1) * page_size < len(user_outputs):
                        current_page += 1
                elif command_input[-1] == 'p':  # Previous page
                    if current_page > 0:
                        current_page -= 1

                # Reset command input and update the right panel
                command_input = ""
                typing_mode = False
                text_entry_panel.clear()
                text_entry_panel.border()
                text_entry_panel.addstr(1, 1, f"> {placeholder_text}", curses.color_pair(2))  # Show placeholder text
                text_entry_panel.refresh()

                # Display outputs for the current page
                right_panel.clear()
                right_panel.border()
                start_index = current_page * page_size
                end_index = start_index + page_size
                for i, output in enumerate(user_outputs[start_index:end_index], start=2):  # Start at row 2 to leave space for the border
                    right_panel.addstr(i, 1, output, curses.color_pair(1))  # Show all user outputs in green
                right_panel.refresh()

            else:
                # Add character to command input
                if chr(key).isprintable():  # Only allow printable characters
                    command_input += chr(key)

            # Display the current command input in the text entry panel
            text_entry_panel.clear()
            text_entry_panel.border()
            text_entry_panel.addstr(1, 1, f"> {command_input}", curses.color_pair(2))  # Show current input in yellow
            text_entry_panel.refresh()
        else:
            # Just refresh the text entry panel if not typing
            text_entry_panel.clear()
            text_entry_panel.border()
            text_entry_panel.addstr(1, 1, f"> {placeholder_text}", curses.color_pair(2))  # Show placeholder text in yellow
            text_entry_panel.refresh()

        # Update other panes, only when not typing
        if not typing_mode:
            top_left.clear()
            top_left.border()
            top_left.addstr(1, 1, "Top Left Pane", curses.color_pair(3))  # Border color
            top_left.refresh()

            bottom_left.clear()
            bottom_left.border()
            bottom_left.addstr(1, 1, "Bottom Left Pane", curses.color_pair(3))  # Border color
            bottom_left.refresh()

            right_panel.border()
            right_panel.refresh()

        # Disable scrolling
        stdscr.scrollok(False)
        stdscr.idlok(False)

curses.wrapper(main)