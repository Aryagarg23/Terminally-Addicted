import curses
import subprocess
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from server.spotify_api import display_current_playback, change_song, next_track, previous_track, pause, play
from server.chatbot import response_generator  
from server.github_api import GitHubIssueManager
from server.todoist import TodoistAPI


def reset_text_bar(text_bar):
    text_bar.clear()
    text_bar.border()
    text_bar.addstr(1, 1, f"> {display_current_playback()}", curses.color_pair(2))  # Show placeholder text
    text_bar.refresh()

def display_or_open_in_vim(panel, content, max_lines, placeholder_text):
    """
    Display content in the panel if it fits, otherwise open it in Vim.
    """
    # Calculate how many lines the content will take
    content_lines = content.splitlines()
    
    if len(content_lines) <= max_lines:
        # If it fits within the available space, display it
        panel.border()
        for i, line in enumerate(content_lines[:max_lines], start=2):  # Start after the border
            panel.addstr(i, 1, line, curses.color_pair(1))
        panel.refresh()
    else:
        # If the response is too long, write to a file and open Vim
        with open('buffer/long_response.txt', 'w') as f:
            f.write(content)
        
        # Close curses, open Vim, then resume curses
        curses.endwin()
        subprocess.run(['vim', 'buffer/long_response.txt'])
        curses.doupdate()

        # Reset the placeholder text after exiting Vim
        panel.border()
        panel.addstr(1, 1, f"> {placeholder_text}", curses.color_pair(2))
        panel.refresh()

def display_titles(top_left, bottom_left, right_panel):
    top_left.addstr(1, 1, "To-Do List", curses.color_pair(3)) 
    bottom_left.addstr(1, 1, "GitHub Issues", curses.color_pair(3)) 
    right_panel.addstr(1, 1, "ChatBot", curses.color_pair(3))  

def display_git_responses(bottom_left, responses):
    bottom_left.border()
    for i, response in enumerate(responses, start=2): 
        bottom_left.addstr(i, 1, response, curses.color_pair(1))  # Show responses in green
    bottom_left.refresh()

def display_tasks(panel, tasks):
    panel.border()
    for i, task in enumerate(tasks, start=2):  # Start displaying tasks from line 2 (after the border)
        panel.addstr(i, 1, task, curses.color_pair(1))  # Display task
        panel.addstr(i + 1, 1, " ", curses.color_pair(1))  # Add an empty line for spacing
        i += 1  # Increment index to account for the additional line
    panel.refresh()