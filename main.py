import os
import directory_walk as dw
import cmd_parse
import database as DB
import schemas
import fuzzy_search


# Search for directories containing '.git' folder indicating a project directory and store in DB
def discover(base_search_dir, max_results, include_hidden=False, max_search_depth=None):
    DB_CONN = DB.create_db_connection("/Users/andrew/Dev/term-mark/database/term_mark.sqlite")
    DB.create_table(DB_CONN)

    sub_dirs = dw.get_subdirectories(base_search_dir, max_results=max_results, include_hidden=include_hidden,
                                     max_search_depth=max_search_depth)
    for dir in sub_dirs:
        if dw.contains_item(dir, ".git"):
            abs_path = dir
            project_name = os.path.basename(dir)
            atime = dw.get_last_access_time(dir)
            mtime = dw.get_last_modification_time(dir)
            is_git = 1
            DB.insert_project(DB_CONN, project_name, abs_path, atime, mtime, is_git)

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


def main():
    args = cmd_parse.parse_args()
    if args.find:
        discover(base_search_dir=args.path, max_results=50, include_hidden=False, max_search_depth=args.depth)
    if args.show:
        term_marks = marshal_term_marks()
        fuzzy_search.display(term_marks)
        # for term_mark in term_marks:
        #     print(term_mark)


if __name__ == "__main__":
    main()
