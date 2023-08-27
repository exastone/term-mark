import argparse


def parse_args():
    parser = argparse.ArgumentParser(prog="\033[32mtm\033[0m",
                                     description="\033[34m  Term-mark, bookmarks for your terminal  \033[0m")

    parser.add_argument("path", nargs="?", type=str, default=".", help="Search path (default '.')")
    parser.add_argument("--show", "-S", action="store_true", help="Show bookmarked projects")
    parser.add_argument("--mark", "-M", action="store_true", help="Toggle bookmark for current directory")
    parser.add_argument("--find", "-F", action="store_true", help="Find directories containing VSC (.git)")
    parser.add_argument("--depth", "-L", type=int, default=2, help="Search depth, used with '--find' (default is 2)",
                        metavar="")
    parser.add_argument("--remove", "-R", action="store_true", help="Remove bookmarks menu")
    parser.add_argument("--init", action="store_true", help="Must be run before using 'tm'")

    return parser.parse_args()
