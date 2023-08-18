from InquirerPy import inquirer
import os


def display(objects):
    # Extract project names from the list of Project objects
    project_names = [project.project_name for project in objects]

    custom_keys = {
        "remove-item": [{"key": "c-d"}],
    }

    result = inquirer.fuzzy(
        message="Book Marked Projects:",
        choices=project_names,
        instruction="[⏎] to select | [Ctrl-d] to remove | ",
        long_instruction="\n"
    ).execute()

    chosen_project_path = next(project["path"] for project in objects if project["name"] == result)
    os.system(f'zsh -i -c "change_dir \'{chosen_project_path}\'"')
