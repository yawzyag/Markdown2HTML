#!/usr/bin/python3
"""markdown to html"""
import sys
import os


def main(argv):
    """markdown to html func"""
    args = sys.argv[1:]
    if (len(args) < 2):
        print("Usage: ./markdown2html.py README.md README.html",
              file=sys.stderr)
        sys.exit(1)
    if (not os.path.isfile(args[0])):
        print("Missing", args[0], file=sys.stderr)
        sys.exit(1)
    exit(0)


if __name__ == "__main__":
    """pass argv to main func"""
    main(sys.argv)
