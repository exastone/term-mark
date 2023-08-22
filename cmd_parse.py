import argparse


def parse_args():
    parser = argparse.ArgumentParser(description="A simple command-line argument example")

    parser.add_argument("path", nargs="?", type=str, default=".", help="Search path (default '.')")
    parser.add_argument("--show", "-S", action="store_true", help="Show bookmarked projects")
    parser.add_argument("--mark", "-M", action="store_true", help="Toggle bookmark for current directory")
    parser.add_argument("--find", "-F", action="store_true", help="Find directories containing VSC (.git)")
    parser.add_argument("--depth", "-L", type=int, default=2, help="Search depth (default is 2)", metavar="")

    return parser.parse_args()
