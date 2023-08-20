import os

from InquirerPy import inquirer


def display(objects):
    # Extract project names from the list of Project objects
    project_names = [project.project_name for project in objects]
    projects = {project.project_name: project.project_path for project in objects}

    project_selection = inquirer.fuzzy(
        message="Book Marked Projects:",
        choices=list(projects.keys()),
        instruction="[⏎] to select",
        long_instruction="\n"
    ).execute()

    selected_path = projects[project_selection]
    str_cmd = f"cd {selected_path}\n"

    home_path = os.environ.get('HOME')
    file_path = os.path.join(home_path, '.tmp', 'termmark.tmp')
    file = open(file_path, 'w')
    file.write(str_cmd)
    file.close()
