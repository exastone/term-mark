import os
import sqlite3

import database as DB
import directory_walk as dw
import menus
import schemas


# Search for directories containing '.git' folder indicating a project directory and store in DB
def discover(base_search_dir, max_results, include_hidden=False, max_search_depth=None):
    sub_dirs = dw.get_subdirectories(base_search_dir, max_results=max_results, include_hidden=include_hidden,
                                     max_search_depth=max_search_depth)
    DB_CONN = DB.create_db_connection(os.environ["TM_PATH_DB"])
    DB.create_table(DB_CONN)
    projects_list = []  # List to store Project objects

    for dir in sub_dirs:
        if dw.contains_item(dir, ".git"):
            # Create a Project object
            project_data = {
                "project_name": os.path.basename(dir),
                "project_path": dir,
                "atime": dw.get_last_access_time(dir),
                "mtime": dw.get_last_modification_time(dir),
                "is_git": 1
            }
            # Append the Project object to the list
            projects_list.append(project_data)

    # Create a new list for projects that should be added
    projects_to_add = []

    # check if project paths exist in DB
    for project in projects_list:
        if not DB.directory_exists(DB_CONN, project["project_path"]):
            projects_to_add.append(project)

    projects_list = projects_to_add  # Replace the original list with the filtered list

    print(f"{len(projects_list)} new projects found")

    for proj in projects_list:
        # Use the insert_project function to insert the Project object
        DB.insert_project(DB_CONN, proj)

    DB_CONN.close()


# fetch term marks from DB and marshal into Project objects
def marshal_term_marks():
    DB_CONN = DB.create_db_connection(os.environ["TM_PATH_DB"])
    term_marks_from_db = DB.fetch_projects(DB_CONN)
    term_mark_objects = []
    for term_mark_row in term_marks_from_db:
        term_mark_object = schemas.Project(*term_mark_row)
        term_mark_objects.append(term_mark_object)
    DB_CONN.close()
    return term_mark_objects


# toggle directory bookmark
def toggle_mark(dir_path):
    try:
        absolute_path = os.path.abspath(dir_path)
        db_path = os.environ["TM_PATH_DB"]

        with DB.create_db_connection(db_path) as conn:
            is_marked = DB.directory_exists(conn, absolute_path)
            if is_marked:
                DB.remove_project_by_path(conn, absolute_path)
                print(f"\033[31m{absolute_path.split('/')[-1]}\033[0m removed from bookmarks")
            else:
                is_git = dw.contains_item(absolute_path, ".git")
                proj = {
                    "project_name": os.path.basename(absolute_path),
                    "project_path": absolute_path,
                    "atime": dw.get_last_access_time(absolute_path),
                    "mtime": dw.get_last_modification_time(absolute_path),
                    "is_git": 1 if is_git else 0
                }
                DB.insert_project(conn, proj)
                print(f"\033[32m{absolute_path.split('/')[-1]}\033[0m added to bookmarks")
    except Exception as e:
        print("An error occurred:", str(e))


def remove_bookmarks():
    try:
        DB_CONN = DB.create_db_connection(os.environ["TM_PATH_DB"])

        # get the list of project objects
        term_mark_objects = marshal_term_marks()
        # get list of selected bookmarks for removal
        selected_bookmarks = menus.select_bookmarks(term_mark_objects)

        confirmation = input("Confirm removal? [Y/n] ")
        if confirmation.strip().lower() == 'y':
            for bookmark in selected_bookmarks:
                DB.remove_project_by_name(DB_CONN, bookmark)
        else:
            print("No bookmarks removed")
        DB_CONN.commit()

        # print("All projects removed successfully.")
    except sqlite3.Error as e:
        print("Error removing projects:", e)
