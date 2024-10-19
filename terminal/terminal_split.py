import curses

def main(stdscr):
    # Initial setup
    curses.curs_set(1)  # Show the cursor
    stdscr.nodelay(False)  # Blocking input for Enter key
    stdscr.clear()

    height, width = stdscr.getmaxyx()

    # Create split panes
    top_left = curses.newwin(height // 2, width // 2, 0, 0)
    top_right = curses.newwin(height // 2, width // 2, 0, width // 2)
    bottom_left = curses.newwin(height // 2, width // 2, height // 2, 0)
    bottom_right = curses.newwin(height // 2, width // 2, height // 2, width // 2)

    # Text entry panel at the bottom
    text_entry_panel = curses.newwin(3, width, height - 3, 0)  # 3 rows high

    # Initial text
    placeholder_text = "Type '/' to enter command mode..."
    command_input = ""  # For storing the current command input
    typing_mode = False  # Flag for typing mode

    # Display the initial state of the panes
    top_left.addstr(1, 1, "Top Left Pane")
    top_right.addstr(1, 1, "Top Right Pane (Output)")
    bottom_left.addstr(1, 1, "Bottom Left Pane")
    bottom_right.addstr(1, 1, "Bottom Right Pane")
    
    # Show placeholder text initially
    text_entry_panel.addstr(1, 1, f"> {placeholder_text}")  # Show placeholder text
    text_entry_panel.border()
    
    top_left.refresh()
    top_right.refresh()
    bottom_left.refresh()
    bottom_right.refresh()
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
                # Put command input into the top right panel
                top_right.clear()
                top_right.border()
                top_right.addstr(1, 1, f"Output: {command_input}")
                top_right.refresh()

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

            bottom_right.clear()
            bottom_right.border()
            bottom_right.addstr(1, 1, "Bottom Right Pane")
            bottom_right.refresh()

        # Disable scrolling
        stdscr.scrollok(False)
        stdscr.idlok(False)

curses.wrapper(main)
