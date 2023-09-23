import argparse


def parse_args():
    parser = argparse.ArgumentParser(prog="\033[32mtm\033[0m",
                                     description="\033[34m  Term-mark, bookmarks for your terminal  \033[0m",
                                     epilog=MORE_INFO,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument("path", nargs="?", type=str, default=".", help="Search path (default '.')")
    parser.add_argument("--init", action="store_true", help="Must be run before using 'tm'")
    parser.add_argument("--mark", "-M", action="store_true", help="Toggle bookmark for current directory")
    parser.add_argument("--show", "-S", action="store_true", help="Show bookmarked projects")
    parser.add_argument("--remove", "-R", action="store_true", help="Remove bookmarks menu. Useful for removing multiple bookmarks")
    parser.add_argument("--find", "-F", action="store_true", help="Find directories containing VSC (.git) and automatically bookmark them")
    parser.add_argument("--depth", "-L", type=int, default=2, help="Search depth, used with '--find' option (default is 2)",
                        metavar="")

    return parser.parse_args()

MORE_INFO = """
Note: By default, glyphs are used as markers. If your shell doesn't support glyphs or your not using a 
patched font, you can disable glyphs and use fall back characters '●' and '○' as marker icons.

To disable glyphs:

add `export TM_USE_GLYPHS=false` to your .zshrc file
then run `source ~/.zshrc`
"""