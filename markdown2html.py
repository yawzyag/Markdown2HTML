#!/usr/bin/python3
"""markdown to html"""
import sys
import os


def write_file(filename="", text=""):
    """write the html file"""
    with open(filename, mode="w", encoding="UTF8") as juanito:
        return juanito.write(text)


def transform_title(string_title=""):
    """transform html format title to html"""
    chars_to_remove = ["#"]
    hsize = 0
    for letter in string_title:
        if (letter == "#"):
            hsize += 1
    html_title = "".join(
        i for i in string_title if i not in chars_to_remove).strip()
    heading_format_start = "<h{}>".format(hsize)
    heading_format_end = "</h{}>".format(hsize)
    return "{}{}{}\n".format(heading_format_start,
                             html_title, heading_format_end)


def read_file(filename="", outputfile=""):
    """read the md file"""
    with open(filename, encoding="UTF8") as juanito:
        finall_text = ""
        for line in juanito:
            if(line.strip()[0] == "#"):
                finall_text += transform_title(line.strip())
        write_file(outputfile, finall_text)


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
    inputFile = args[0]
    outputfile = args[1]
    read_file(inputFile, outputfile)
    exit(0)


if __name__ == "__main__":
    """pass argv to main func"""
    main(sys.argv)
