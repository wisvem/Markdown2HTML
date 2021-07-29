#!/usr/bin/python3
"""Markdown to html module"""


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


if __name__ == '__main__':
    from os.path import isfile
    from sys import argv, stderr

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
            if not line.isspace():
                temp_file.append(
                    check_headings(
                        html_list(html_list(line, "uli"), "oli")
                    )
                )

    with open(f"./{html_file}", 'w') as html:
        html.writelines(list_wrapper(list_wrapper(
            temp_file, 'ul'), 'ol')
        )
        html.write('\n')

    exit(0)
