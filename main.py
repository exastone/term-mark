import os
import sys

import database
import directory_walk as dw
import cmd_parse
import database as DB
import schemas
import fuzzy_search


# Search for directories containing '.git' folder indicating a project directory and store in DB
def discover(base_search_dir, max_results, include_hidden=False, max_search_depth=None):
    sub_dirs = dw.get_subdirectories(base_search_dir, max_results=max_results, include_hidden=include_hidden,
                                     max_search_depth=max_search_depth)
    DB_CONN = DB.create_db_connection("/Users/andrew/Dev/term-mark/database/term_mark.sqlite")
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

    print(f"{len(projects_list)} projects found")

    for proj in projects_list:
        # Insert the Project object's attributes into the database
        DB.insert_project(DB_CONN, proj["project_name"], proj["project_path"], proj["atime"], proj["mtime"],
                          proj["is_git"])

    DB_CONN.close()


# fetch term marks from DB and marshal into Project objects
def marshal_term_marks():
    # DB_CONN = DB.create_db_connection("database/term_mark.sqlite")
    DB_CONN = DB.create_db_connection("/Users/andrew/Dev/term-mark/database/term_mark.sqlite")
    term_marks_from_db = DB.fetch_projects(DB_CONN)
    term_mark_objects = []
    for term_mark_row in term_marks_from_db:
        term_mark_object = schemas.Project(*term_mark_row)
        term_mark_objects.append(term_mark_object)
    DB_CONN.close()
    return term_mark_objects


def toggle_mark(dir_path):
    absolute_path = os.path.abspath(dir_path)
    DB_CONN = DB.create_db_connection("/Users/andrew/Dev/term-mark/database/term_mark.sqlite")
    is_marked = database.directory_exists(DB_CONN, absolute_path)
    if is_marked:
        database.remove_project_by_path(DB_CONN, absolute_path)
        print(f"../{absolute_path.split('/')[-1]} bookmark removed")
        DB_CONN.close()
    else:
        is_git = dw.contains_item(absolute_path, ".git")
        # Create a Project object
        proj = {
            "project_name": os.path.basename(absolute_path),
            "project_path": absolute_path,
            "atime": dw.get_last_access_time(absolute_path),
            "mtime": dw.get_last_modification_time(absolute_path),
            "is_git": 1 if is_git else 0
        }
        DB.insert_project(DB_CONN, proj["project_name"], proj["project_path"], proj["atime"], proj["mtime"],
                          proj["is_git"])
        DB_CONN.close()


def main():
    args = cmd_parse.parse_args()
    # print(f"args {args}")
    if args.find:
        absolute_path = os.path.abspath(args.path)
        discover(base_search_dir=absolute_path, max_results=50, include_hidden=False, max_search_depth=args.depth)
        # 1 -> parent shell script does not proceed
        return sys.exit(1)
    if args.show:
        term_marks = marshal_term_marks()
        if len(term_marks) != 0:
            fuzzy_search.display(term_marks)
            # 1 -> parent shell script proceeds
            return sys.exit(0)
        else:
            print("No bookmarks found, run 'tm --find <directory>' to search for projects under <directory>")
            return sys.exit(1)
    if args.mark:
        toggle_mark(dir_path=args.path)

        # for mark in term_marks:
        #     # Using dir() to print all fields
        #     for attribute in dir(mark):
        #         if not attribute.startswith("__"):
        #             value = getattr(mark, attribute)
        #             print(attribute, "=", value)
        # # print(term_marks)


if __name__ == "__main__":
    main()
