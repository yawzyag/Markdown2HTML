#!/usr/bin/python3
"""markdown to html"""
import sys
import getopt
import os


def main(argv):
    """markdown to func"""
    inputfile = ''
    outputfile = ''
    try:
        opts, args = getopt.getopt(argv, "hi:o:", ["ifile=", "ofile="])
        if (len(args) < 2):
            # print to standart error
            print("Usage: ./markdown2html.py README.md README.html",
                  file=sys.stderr)
            sys.exit(1)
        if (not os.path.isfile(args[0])):
            print("Missing", args[0], file=sys.stderr)
            sys.exit(1)
    except Exception as ex:
        print(ex)
    exit(0)


if __name__ == "__main__":
    """pass to main func"""
    main(sys.argv[1:])
