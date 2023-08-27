import os
import sys

from term_mark import menus, cmd_parse
from term_mark.constants import TERMINATE, PROCEED
from term_mark.tm_functions import discover, marshal_term_marks, toggle_mark, remove_bookmarks, init


def main():
    os.environ["TM_PATH"] = os.path.dirname(os.path.abspath(__file__))
    os.environ["TM_PATH_DB"] = os.path.join(os.environ["TM_PATH"], "term_mark.sqlite")

    args = cmd_parse.parse_args()

    # for debug
    # print(f"args {args}")

    if args.init:
        init()
    if args.find:
        absolute_path = os.path.abspath(args.path)
        discover(base_search_dir=absolute_path, max_results=50, include_hidden=False, max_search_depth=args.depth)
        # 1 -> parent shell script does not proceed
        return sys.exit(TERMINATE)
    if args.show:
        term_marks = marshal_term_marks()
        if len(term_marks) != 0:
            menus.select_bookmark_from_fuzzy(term_marks)
            # 0 -> parent shell script proceeds
            return sys.exit(PROCEED)
        else:
            print("No bookmarks found, run 'tm --find <directory>' to search for projects under <directory>")
            return sys.exit(TERMINATE)
    if args.mark:
        toggle_mark(dir_path=args.path)
    if args.remove:
        remove_bookmarks()


if __name__ == "__main__":
    main()
