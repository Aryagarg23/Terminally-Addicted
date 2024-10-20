import curses
import subprocess
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from server.spotify_api import display_current_playback, change_song, next_track, previous_track, pause, play
from server.chatbot import response_generator  
from server.github_api import GitHubIssueManager
from server.todoist import TodoistAPI
from terminal.helpers import reset_text_bar, display_or_open_in_vim, display_titles, display_git_responses, display_tasks

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
    command_input = ""  # For storing the current command input
    typing_mode = False  # Flag for typing mode

    # List to store user outputs and git responses
    user_outputs = []
    git_responses = []  # New list to store git command responses
    current_page = 0  # Track the current page
    page_size = 10  # Number of outputs per page

    display_titles(top_left, bottom_left, right_panel)

    # Show placeholder text initially
    text_entry_panel.addstr(1, 1, f"> {display_current_playback()}", curses.color_pair(2))  # Show placeholder text in yellow
    text_entry_panel.border()
    
    top_left.refresh()
    bottom_left.refresh()
    right_panel.refresh()
    text_entry_panel.refresh()

    manager = GitHubIssueManager()
    todoist = TodoistAPI()
    
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
                if command_input.startswith("/set env"):
                    # Open the .env file in Vim
                    curses.endwin()  # End the curses session before opening Vim
                    subprocess.run(['vim', 'server/.env'])  # Open .env file
                    stdscr.clear()  # Clear the screen after Vim is closed
                    stdscr.refresh()
                    command_input = ""
                    continue  # Continue t`he main loop

                # If the command is "/chat"
                if command_input.startswith("/chat"):
                    # Handle /chat -v for Vim input
                    if command_input == "/chat -l":
                        # Close the curses interface temporarily and open Vim
                        curses.endwin()  # Close the curses window
                        subprocess.run(['vim', 'buffer/chat_current_input.txt'])
                        curses.doupdate()  # Restart the curses interface

                        # Call response_generator for a long response
                        if command_input.startswith('/chat -l -cls'):
                            keep_his = False
                        else:
                            keep_his = True

                        bot_response = response_generator(keep_history=keep_his, short_or_long=1)

                        # Add Vim output and bot response to user outputs
                        user_outputs.append(f"Bot: {bot_response} \n  ")

                        # Calculate available lines for the right panel
                        max_lines = height - 6  # Subtracting space for border and other UI elements

                        display_titles(top_left, bottom_left, right_panel)
                        display_or_open_in_vim(right_panel, bot_response, max_lines, display_current_playback())
                    
                    elif command_input.startswith('/chat -s'):
                        # Save short input to file for short response
                        with open('buffer/chat_current_input.txt', 'w+') as f:
                            f.write(command_input[9:])  # Save user input after `/chat -s`

                        if command_input.startswith('/chat -l -cls'):
                            keep_his = False
                        else:
                            keep_his = True

                        bot_response = response_generator(keep_history=keep_his, short_or_long=1)

                        # Add short response to user outputs
                        user_outputs.append(f"User: {command_input[9:]}")
                        user_outputs.append(f"Bot: {bot_response}")

                        # Calculate available lines for the right panel
                        max_lines = height - 6  # Subtracting space for border and other UI elements

                        # Display outputs or open in Vim if too long
                        display_titles(top_left, bottom_left, right_panel)
                        display_or_open_in_vim(right_panel, f"User: {command_input[9:]}\n  Bot: {bot_response}", max_lines, display_current_playback())

                        # Display outputs for the current page
                        right_panel.border()
                        start_index = current_page * page_size
                        end_index = start_index + page_size
                        for i, output in enumerate(user_outputs[start_index:end_index], start=2):  # Start at row 2 to leave space for the border
                            right_panel.addstr(i, 1, output, curses.color_pair(1))  # Show all user outputs in green
                        right_panel.refresh()
                elif command_input.startswith("/sp"):
                    if command_input.startswith("/sp -cs"):
                        song_name = command_input[8:]
                        change_song(song_name)
                        reset_text_bar(text_entry_panel)
                    elif command_input.startswith("/sp -next"):
                        next_track()
                        reset_text_bar(text_entry_panel)
                    elif command_input.startswith("/sp -prev"):
                        try:
                            previous_track()
                            reset_text_bar(text_entry_panel)
                        except:
                            reset_text_bar(text_entry_panel)
                    elif command_input.startswith("/sp -ps"):
                        pause()
                        reset_text_bar(text_entry_panel)
                    elif command_input.startswith("/sp -pl"):
                        try:
                            play()
                        except:
                            reset_text_bar(text_entry_panel)
                        reset_text_bar(text_entry_panel)
                elif command_input.startswith("/git"):
                    response = None  # Initialize response variable
                    if command_input.startswith("/git create"):
                        # Extract the command arguments from the input
                        args = command_input[11:].strip().split(' --')
                        title = args[0]
                        body = None
                        labels = []

                        # Check for additional arguments like body and labels
                        if len(args) > 1:
                            for arg in args[1:]:
                                if arg.startswith('labels='):
                                    labels = arg[len('labels='):].split(',')
                                elif body is None:
                                    body = arg.strip()  # Get the first argument after the title as body

                        # Create an issue
                        response = manager.create_issue(title, body, labels)

                    elif command_input.startswith("/git close"):
                        issue_number = command_input[11:].strip()
                        response = manager.close_issue(issue_number)

                    elif command_input.startswith("/git comment"):
                        # Extract the issue number and comment text
                        parts = command_input[13:].strip().split(' ', 1)
                        issue_number = parts[0]
                        comment = parts[1] if len(parts) > 1 else ''
                        response = manager.comment_on_issue(issue_number, comment)

                    elif command_input.startswith("/git list"):
                        state_arg = command_input[10:].strip()
                        state = 'open'  # Default to 'open'
                        
                        if state_arg.startswith('--state'):
                            state = state_arg.split('=')[1] if '=' in state_arg else 'open'
                        
                        response = manager.list_issues(state)

                    elif command_input.startswith("/git update"):
                        args = command_input[12:].strip().split(' --')
                        issue_number = args[0]
                        new_title = None
                        new_body = None

                        # Check for new title and body
                        for arg in args[1:]:
                            if arg.startswith('title='):
                                new_title = arg[len('title='):]
                            elif arg.startswith('body='):
                                new_body = arg[len('body='):]

                        response = manager.update_issue(issue_number, new_title, new_body)

                    elif command_input.startswith("/git search"):
                        label = command_input[12:].strip()
                        response = manager.search_issues_by_label(label)

                    elif command_input.startswith("/git set repo"):
                        parts = command_input[14:].strip().split(' ')
                        if len(parts) == 2:
                            owner, repo_name = parts
                            manager.set_owner_repo(owner, repo_name)
                            response = f"Repository set to: {owner}/{repo_name}"
                        else:
                            response = "Invalid format. Use /git set repo owner/repo_name"
                    # Add response to git_responses if there is one
                    if response:
                        git_responses.append(response)
                        display_git_responses(bottom_left, git_responses)  # Update the bottom left pane

                elif command_input.startswith("/todo list"):
                    tasks = todoist.get_tasks()  # Fetch tasks once
                    total_tasks = len(tasks)  # Update total tasks count
                    # Display first four tasks or notify if less than four
                    display_tasks(top_left, tasks[current_page:current_page + page_size])

                elif command_input.startswith("/todo add "):
                    # Extract the task name and create a new task
                    task_name = command_input[10:]  # Get the task name after the command
                    response = todoist.create_task(task_name)

                elif command_input == "/todo list -more":
                    # Show next set of tasks if available
                    current_page += page_size
                    if current_page < total_tasks:
                        display_tasks(top_left, tasks[current_page:current_page + page_size])
                    else:
                        # No more tasks available
                        display_tasks(top_left, ["No more tasks available."])
                    

                # Reset command input and show placeholder again
                command_input = ""
                typing_mode = False
                reset_text_bar(text_entry_panel)

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
            reset_text_bar(text_entry_panel)

        # Update other panes, only when not typing
        if not typing_mode:
            reset_text_bar(text_entry_panel)
            top_left.border()
            top_left.refresh()

            bottom_left.border()
            bottom_left.refresh()

            right_panel.border()
            right_panel.refresh()

        # Disable scrolling
        stdscr.scrollok(False)
        stdscr.idlok(False)

curses.wrapper(main)