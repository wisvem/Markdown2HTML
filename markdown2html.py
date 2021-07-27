#!/usr/bin/python3

from os.path import isfile
from sys import argv, stderr

if len(argv) != 3:
    stderr.write('Usage: ./markdown2html.py README.md README.html\n')
    exit(1)

filename = argv[1]
if not isfile(f"./{filename}"):
    stderr.write(f"Missing {filename}\n")
    exit(1)
output_filename = argv[2]
exit(0)
