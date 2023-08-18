import argparse


def parse_args():
    parser = argparse.ArgumentParser(description="A simple command-line argument example")

    parser.add_argument("path", nargs="?", type=str, default=".", help="Search path")
    parser.add_argument("--depth", "-L", type=int, default=2, help="Search depth (default is 2)", metavar="")
    parser.add_argument("--find", "-F", type=str, help="Find directories containing VSC (.git)", metavar="")
    parser.add_argument("--show", "-S", action="store_true", help="Show book marked projects")
    parser.add_argument("--verbose", "-v", action="store_true", help="Include files in output (not used)")

    return parser.parse_args()
