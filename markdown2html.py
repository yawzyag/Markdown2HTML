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
    hsize = 0
    chars_to_remove = ["#"]
    for letter in string_title:
        if (letter == "#"):
            hsize += 1
    html_title = "".join(
        i for i in string_title if i not in chars_to_remove).strip()
    heading_format_start = "<h{}>".format(hsize)
    heading_format_end = "</h{}>".format(hsize)
    return "{}{}{}\n".format(heading_format_start,
                             html_title, heading_format_end)


def transform_list(string_list=""):
    """transform html format list to html"""
    chars_to_remove = ["-"]
    string_list = "".join(
        i for i in string_list if i not in chars_to_remove).strip()
    return "<li>{}</li>\n".format(string_list)


def transform_order_list(string_list=""):
    """transform html format list to html"""
    chars_to_remove = ["*"]
    string_list = "".join(
        i for i in string_list if i not in chars_to_remove).strip()
    return "<li>{}</li>\n".format(string_list)


def transform_paragraph(string_paragraph=""):
    """transform html format list to html"""
    return "{}\n".format(string_paragraph.strip())


def read_file(filename="", outputfile=""):
    """read the md file"""
    with open(filename, encoding="UTF8") as juanito:
        finall_text = ""
        lines = [line for line in juanito]
        prev_line = ""
        i = 0
        for line in lines:
            if (lines[i-1]):
                prev_line = lines[i-1]
            temporal_text = ""
            if(len(line.strip()) > 1 and line.strip()[0] == "#"):
                finall_text += transform_title(line.strip())
            elif (len(line.strip()) > 1 and line.strip()[0] == "-"):
                if (finall_text[-6:-1] == "</ul>"):
                    finall_text = finall_text[0:-6]
                else:
                    temporal_text += "<ul>\n"
                temporal_text += transform_list(line.strip())
                temporal_text += "</ul>\n"
            elif (len(line.strip()) > 1 and line.strip()[0] == "*"):
                if (finall_text[-6:-1] == "</ol>"):
                    finall_text = finall_text[0:-6]
                else:
                    temporal_text += "<ol>\n"
                temporal_text += transform_order_list(line.strip())
                temporal_text += "</ol>\n"
            elif (len(line.strip()) > 1 and line.strip()[0].isalpha()):
                if (len(prev_line.strip()) > 1 and
                        finall_text[-6:-1].strip() == "</p>"):
                    finall_text = finall_text[0:-6]
                    temporal_text += "\n<br />\n"
                else:
                    temporal_text += "<p>\n"
                temporal_text += transform_paragraph(line)
                temporal_text += "</p>\n"
            else:
                finall_text += ""
            finall_text += temporal_text
            i += 1
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
