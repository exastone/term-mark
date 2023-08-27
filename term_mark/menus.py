import os
import sys

from term_mark.InquirerPy.InquirerPy import inquirer
from term_mark.InquirerPy.InquirerPy.base.control import Choice

from term_mark.constants import TERMINATE


def write_selected_path_to_file(selected_path):
    """Write the selected path to a temporary file."""
    home_path = os.path.expanduser('~')
    tmp_directory = os.path.join(home_path, '.tmp')

    # Create the directory if it doesn't exist
    if not os.path.exists(tmp_directory):
        os.makedirs(tmp_directory)

    file_path = os.path.join(tmp_directory, 'termmark.tmp')

    with open(file_path, 'w') as file:
        file.write(f"cd \"{selected_path}\"\n")


def select_bookmark_from_fuzzy(objects):
    """Select a project from a list of Project objects."""
    projects = {project.project_name: project.project_path for project in objects}
    choices = [
        Choice(project.project_name, name=project.project_name, instruction=project.project_path)
        for project in objects
    ]
    choices = sorted(choices, key=lambda choice: choice.name.lower())

    try:
        project_selection = inquirer.fuzzy(
            message="",
            qmark="",
            amark="",
            marker_pl=" ",
            choices=choices,
            instruction="[⏎] go to selected | [Ctrl+c] cancel",
            long_instruction="\n"
        ).execute()

        # handles case where user enters search with no matches and hits enter
        if project_selection is not None:
            selected_path = projects[project_selection]
            write_selected_path_to_file(selected_path)
        else:
            sys.exit(TERMINATE)
    except KeyboardInterrupt:
        sys.exit(TERMINATE)


def select_bookmarks(objects):
    """Select bookmarks for removal."""
    choices = [
        Choice(project.project_name, name=project.project_name, instruction=project.project_path)
        for project in objects
    ]
    choices = sorted(choices, key=lambda choice: choice.name.lower())

    try:
        selections = inquirer.checkbox(
            message="",
            qmark="",
            amark="",
            enabled_symbol="",
            disabled_symbol="",
            instruction="[Space] add to selection | [Ctrl+r] toggle selection all",
            choices=choices,
            vi_mode=True,
            transformer=lambda _: f"{len(_)} bookmark{'s' if len(_) > 1 else ''} selected for removal",
        ).execute()
    except KeyboardInterrupt:
        sys.exit(TERMINATE)

    return selections
