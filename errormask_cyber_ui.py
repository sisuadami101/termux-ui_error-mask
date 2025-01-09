import os
import curses
import time
import shutil
import requests
from getpass import getpass

# Global Variables
current_path = os.getcwd()
selected_files = []
password = "cyber_expert_2023"
icons = {"file": "[FILE]", "dir": "[DIR]", "exec": "[EXEC]"}

# Banner Message
BANNER_TEXT = r"""
███████╗███████╗██████╗ ███████╗███████╗██████╗ 
██╔════╝██╔════╝██╔══██╗██╔════╝██╔════╝██╔══██╗
███████╗█████╗  ██████╔╝███████╗█████╗  ██████╔╝
╚════██║██╔══╝  ██╔═══╝ ╚════██║██╔══╝  ██╔═══╝ 
███████║███████╗██║     ███████║███████╗██║     
╚══════╝╚══════╝╚═╝     ╚══════╝╚══════╝╚═╝     
[ PROFESSIONAL CYBER EXPERT TERMINAL UI ]
"""

# Animation Effect
def sci_fi_animation(stdscr, message, delay=0.1):
    stdscr.clear()
    height, width = stdscr.getmaxyx()
    for i, char in enumerate(message):
        stdscr.addstr(height // 2, (width - len(message)) // 2 + i, char, curses.color_pair(1))
        stdscr.refresh()
        time.sleep(delay)
    time.sleep(1)

# Show Banner
def show_banner(stdscr):
    height, width = stdscr.getmaxyx()
    stdscr.clear()
    for i, line in enumerate(BANNER_TEXT.splitlines()):
        stdscr.addstr(i + 2, (width - len(line)) // 2, line, curses.color_pair(1))
    stdscr.addstr(height - 2, 0, "Press any key to start...", curses.color_pair(1))
    stdscr.refresh()
    stdscr.getch()

# Handle GitHub Cloning
def github_clone(stdscr):
    stdscr.clear()
    curses.echo()
    stdscr.addstr(0, 0, "Enter GitHub Repo URL to Clone: ")
    repo_url = stdscr.getstr(1, 0).decode("utf-8")
    stdscr.addstr(2, 0, f"Cloning {repo_url}...")
    stdscr.refresh()
    os.system(f"git clone {repo_url}")
    stdscr.addstr(3, 0, "Clone Completed! Press any key to return.")
    stdscr.getch()
    curses.noecho()

# File Preview
def preview_file(stdscr, file_path):
    stdscr.clear()
    try:
        with open(file_path, "r") as file:
            content = file.read(500)
        stdscr.addstr(0, 0, content[: curses.COLS - 1])
    except Exception as e:
        stdscr.addstr(0, 0, f"Error: {e}")
    stdscr.addstr(curses.LINES - 1, 0, "Press any key to return.")
    stdscr.getch()

# File Manager
def file_manager(stdscr):
    global current_path
    curses.curs_set(0)
    height, width = stdscr.getmaxyx()
    current_row = 0
    files = os.listdir(current_path)

    while True:
        stdscr.clear()
        files = os.listdir(current_path)
        stdscr.addstr(0, 0, f"Path: {current_path}", curses.color_pair(1))
        stdscr.addstr(1, 0, "Commands: [Enter: Open] [D: Delete] [N: New Dir] [G: Git Clone] [Esc: Exit]", curses.color_pair(1))

        for idx, file in enumerate(files):
            icon = icons["dir"] if os.path.isdir(os.path.join(current_path, file)) else icons["file"]
            if os.access(os.path.join(current_path, file), os.X_OK):
                icon = icons["exec"]
            if idx == current_row:
                stdscr.addstr(idx + 2, 0, f"{icon} {file}", curses.color_pair(2) | curses.A_BOLD)
            else:
                stdscr.addstr(idx + 2, 0, f"{icon} {file}", curses.color_pair(1))

        stdscr.refresh()
        key = stdscr.getch()

        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(files) - 1:
            current_row += 1
        elif key == ord("\n"):
            selected = os.path.join(current_path, files[current_row])
            if os.path.isdir(selected):
                current_path = selected
                current_row = 0
            else:
                preview_file(stdscr, selected)
        elif key == ord("D") or key == ord("d"):
            os.remove(os.path.join(current_path, files[current_row]))
        elif key == ord("N") or key == ord("n"):
            curses.echo()
            stdscr.addstr(height - 1, 0, "Enter New Directory Name: ")
            dir_name = stdscr.getstr(height - 1, 25).decode("utf-8")
            os.mkdir(os.path.join(current_path, dir_name))
            curses.noecho()
        elif key == ord("G") or key == ord("g"):
            github_clone(stdscr)
        elif key == 27:
            break

# Password Protection
def password_protection():
    user_password = getpass("Enter Password: ")
    if user_password != password:
        print("Wrong Password! Exiting...")
        exit()

# Main Function
def main():
    password_protection()
    curses.wrapper(lambda stdscr: (sci_fi_animation(stdscr, "Welcome to Cyber Expert UI"), show_banner(stdscr), file_manager(stdscr)))

if __name__ == "__main__":
    main()
