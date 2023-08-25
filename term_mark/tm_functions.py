import os
import sqlite3

from term_mark import schemas
from term_mark import database as DB, menus, directory_walk as dw


# Function to check if a table exists and create it if not
def check_and_create_table(connection):
    if not DB.table_exists(connection):
        DB.create_table(connection)


# Function to process discovered projects
def process_projects(connection, projects_list):
    projects_to_add = []

    for project in projects_list:
        if not DB.directory_exists(connection, project["project_path"]):
            projects_to_add.append(project)

    print(f"{len(projects_to_add)} new projects found")

    for proj in projects_to_add:
        DB.insert_project(connection, proj)


# Search for directories containing '.git' folder indicating a project directory and store in DB
def discover(base_search_dir, max_results, include_hidden=False, max_search_depth=None):
    sub_dirs = dw.get_subdirectories(base_search_dir, max_results=max_results, include_hidden=include_hidden,
                                     max_search_depth=max_search_depth)

    DB_CONN = DB.create_db_connection(os.environ["TM_PATH_DB"])
    check_and_create_table(DB_CONN)

    projects_list = []

    for dir in sub_dirs:
        if dw.contains_item(dir, ".git"):
            project_data = {
                "project_name": os.path.basename(dir),
                "project_path": dir,
                "atime": dw.get_last_access_time(dir),
                "mtime": dw.get_last_modification_time(dir),
                "is_git": 1
            }
            projects_list.append(project_data)

    process_projects(DB_CONN, projects_list)

    DB_CONN.close()


# Fetch term marks from DB and marshal into Project objects
def marshal_term_marks():
    db_path = os.environ["TM_PATH_DB"]
    with DB.create_db_connection(db_path) as conn:
        check_and_create_table(conn)  # Check and create table if necessary
        term_marks_from_db = DB.fetch_projects(conn)
        term_mark_objects = []
        for term_mark_row in term_marks_from_db:
            term_mark_object = schemas.Project(*term_mark_row)
            term_mark_objects.append(term_mark_object)
    return term_mark_objects


# Toggle directory bookmark
def toggle_mark(dir_path):
    try:
        absolute_path = os.path.abspath(dir_path)
        db_path = os.environ["TM_PATH_DB"]

        with DB.create_db_connection(db_path) as conn:
            check_and_create_table(conn)  # Check and create table if necessary
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
        db_path = os.environ["TM_PATH_DB"]
        with DB.create_db_connection(db_path) as conn:
            check_and_create_table(conn)  # Check and create table if necessary

            term_mark_objects = marshal_term_marks()
            selected_bookmarks = menus.select_bookmarks(term_mark_objects)

            confirmation = input("Confirm removal? [Y/n] ")
            if confirmation.strip().lower() == 'y':
                for bookmark in selected_bookmarks:
                    DB.remove_project_by_name(conn, bookmark)
            else:
                print("No bookmarks removed")
            conn.commit()
    except sqlite3.Error as e:
        print("Error removing projects:", e)
