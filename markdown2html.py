#!/usr/bin/python3
"""Markdown to html module"""

from os.path import isfile
from re import search
from sys import argv, stderr


def check_headings(string):
    """add headings function"""
    h_tag, i = "#", 0
    for letter in string:
        if (letter == h_tag):
            i += 1
        elif letter in [" ", None, "\n"]:
            break
        else:
            return string
    return f'<h{i}>{string[i+1:].strip()}</h{i}>\n' if 0 < i < 7 else string


def html_list(string, list_type):
    """Convert -/* lines to li elements"""
    li_tag = '-' if list_type == 'uli' else '*'
    i = 0
    for letter in string:
        if (letter == li_tag):
            i += 1
        elif letter in [" ", None, "\n"]:
            break
        else:
            return string
    html = f'<li>{string[i+1:].strip()}</li>\n'
    return list_type+html if 0 < i < 2 else string


def list_wrapper(str_lst, ulol):
    """Wrap list with ul/ol"""
    list_sw = True
    result = []
    for line in range(len(str_lst)):
        start_with_list = str_lst[line].startswith(f'{ulol}i<')
        if start_with_list and list_sw:
            str_lst[line] = str_lst[line].replace(f'{ulol}i<', '<')
            result.append(f'<{ulol}>\n{str_lst[line]}')
            list_sw = False
        elif start_with_list and not list_sw:
            str_lst[line] = str_lst[line].replace(f'{ulol}i<', '<')
            result.append(str_lst[line])
        elif not start_with_list and not list_sw:
            result.append(f'</{ulol}>\n{str_lst[line]}')
            list_sw = True
        elif not start_with_list and list_sw:
            result.append(str_lst[line])
    result.append(f'</{ulol}>') if not list_sw else None
    return result


def paragraph(file):
    """Set html <p> paragraph"""
    p = True
    for line in range(len(file)):
        is_empty = file[line].isspace()
        is_html = search(r'<\/?[a-z][\s\S]*>', file[line])
        if p and not is_html and not is_empty:
            file[line] = f'<p>\n{file[line]}'
            p = False
        elif (is_html or is_empty) and not p:
            file[line] = f'</p>\n{file[line]}'
            p = True
        elif not is_empty and not is_html and not p:
            file[line] = f'<br/>\n{file[line]}'
    if not p:
        file.append('</p>')
    return file


def main():
    """Entry point"""
    if len(argv) != 3:
        stderr.write("Usage: ./markdown2html.py README.md README.html\n")
        exit(1)
    md_file = argv[1]
    if not isfile(f"./{md_file}"):
        stderr.write(f"Missing {md_file}\n")
        exit(1)
    html_file = argv[2]
    temp_file = []
    with open(f"./{md_file}", 'r') as f:
        for line in f.readlines():
            temp_file.append(
                check_headings(
                    html_list(html_list(line, "uli"), "oli")))
    temp_file = list_wrapper(list_wrapper(temp_file, 'ul'), 'ol')
    temp_file = paragraph(temp_file)
    with open(f"./{html_file}", 'w') as html:
        a = list(filter(lambda x: not x.isspace(), temp_file))
        html.writelines(a)
        html.write('\n')
    exit(0)


if __name__ == '__main__':
    main()
