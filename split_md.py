#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import re

def split_markdown_file(input_filename):
    with open(input_filename, 'r') as file:
        contents = file.read()
        # Split based on lines that only include "* * *"
        parts = re.split(r'\n\* \* \*\n', contents)

    for i, part in enumerate(parts):
        # remove leading and trailing whitespace, including newlines
        part = part.strip()
        # only create a file if the part is not empty
        if part:
            output_filename = f"{input_filename.split('.')[0]}_part{i}.md"
            with open(output_filename, 'w') as file:
                file.write(part)

def main():
    parser = argparse.ArgumentParser(description='Split a markdown file at each line containing only "* * *".')
    parser.add_argument('input_filename', type=str, help='The markdown file to split.')

    args = parser.parse_args()
    split_markdown_file(args.input_filename)

if __name__ == "__main__":
    main()
