#!/usr/bin/python3
"""markdown to html"""
import sys
import os
import re
import hashlib


def nth_repl(s, sub, repl, n):
    find = s.find(sub)
    i = find != -1
    while find != -1 and i != n:
        find = s.find(sub, find + 1)
        i += 1
    if i == n:
        return s[:find] + repl + s[find+len(sub):]
    return s


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


def transform_bold(string_bold=""):
    text_re = re.findall(r"\*{2}(.*?)\*{2}", string_bold)
    for pattern in text_re:
        patterncopy = "{}{}{}".format("<b>", pattern, "</b>")
        string_bold = string_bold.replace("**"+pattern+"**", patterncopy)
    return string_bold


def transform_em(string_em=""):
    count = string_em.count("__")
    for i in range(count):
        if(i % 2 != 0):
            string_em = nth_repl(string_em, "__", "</em>", 1)
        else:
            string_em = nth_repl(string_em, "__", "<em>", 1)
    return string_em


def transform_to_md5(text_to_md5=""):
    m = hashlib.md5()
    m.update(text_to_md5.encode('utf-8'))
    return m.hexdigest()


def transform_line_md5(string_to_transform=""):
    text_re = re.findall(r"\[\[[^\]]*\]\]", string_to_transform)
    for pattern in text_re:
        copypattern = pattern.replace("[[", "")
        copypattern = copypattern.replace("]]", "")
        md5 = transform_to_md5(copypattern)
        string_to_transform = string_to_transform.replace(pattern, md5)
    return string_to_transform


def replace_case(old, new, str, caseinsentive=False):
    if caseinsentive:
        return str.replace(old, new)
    else:
        return re.sub(re.escape(old), new, str, flags=re.IGNORECASE)


def transform_remove_c(string_to_transform=""):
    text_re = re.findall(r"\(\([^\)]*\)\)", string_to_transform)
    for pattern in text_re:
        patterncopy = replace_case("c", '', pattern)
        patterncopy = patterncopy.replace("((", "")
        patterncopy = patterncopy.replace("))", "")
        string_to_transform = string_to_transform.replace(pattern, patterncopy)
    return string_to_transform


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
            elif (len(line.strip()) > 1 and line.strip()[0] ==
                    "*" and line.strip()[1] != "*"):
                if (finall_text[-6:-1] == "</ol>"):
                    finall_text = finall_text[0:-6]
                else:
                    temporal_text += "<ol>\n"
                temporal_text += transform_order_list(line.strip())
                temporal_text += "</ol>\n"
            elif (len(line.strip()) > 1 and line.strip()[0] != ""):
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
            if (re.search(r"\*{2}(.*?)\*{2}", temporal_text)):
                temporal_text = transform_bold(temporal_text)
            if (temporal_text.count("__") >= 2):
                temporal_text = transform_em(temporal_text)
            if (re.search(r"\[\[[^\]]*\]\]", temporal_text)):
                temporal_text = transform_line_md5(temporal_text)
            if (re.search(r"\(\([^\)]*\)\)", temporal_text)):
                temporal_text = transform_remove_c(temporal_text)
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
