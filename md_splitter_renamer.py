#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import os
import re
from datetime import datetime

def split_markdown_file(input_filename):
    with open(input_filename, 'r') as file:
        contents = file.read()
        parts = re.split(r'\n\* \* \*\n', contents)

    for i, part in enumerate(parts):
        part = part.strip()
        if part:
            output_filename = f"{input_filename.split('.')[0]}_part{i}.md"
            output_filename = get_unique_filename(output_filename)
            with open(output_filename, 'w') as file:
                file.write(part)
            rename_file(output_filename)

def get_new_name(path):
    with open(path, 'r') as file:
        lines = file.readlines()

    first_section = ""
    creation_time = ""
    for line in lines:
        if line.startswith('# '):
            first_section = line[2:].strip()
            first_section = first_section.replace("'", "")
            first_section = first_section.replace('"', "")
            first_section = re.sub(r"[ .,:;/]", "_", first_section)
            first_section = first_section.replace("__", "_")
            first_section = first_section.rstrip("_")
        if line.startswith('Creation Time:'):
            creation_time = line[len('Creation Time:'):].strip().split()[0]
            creation_time = datetime.strptime(creation_time, '%Y-%m-%d')
            creation_time = creation_time.strftime('%Y_%m%d')
        if first_section and creation_time:
            break

    return f'{first_section}_{creation_time}.md' if first_section and creation_time else None

def get_unique_filename(filename):
    directory, name = os.path.split(filename)
    base, ext = os.path.splitext(name)

    counter = 1
    while os.path.exists(filename):
        filename = os.path.join(directory, f"{base}_{counter}{ext}")
        counter += 1

    return filename

def rename_file(path):
    if not os.path.exists(path):
        print(f"File {path} does not exist.")
        return

    new_name = get_new_name(path)
    if not new_name:
        print(f"Could not determine new name for file {path}.")
        return

    directory = os.path.dirname(path)
    new_path = get_unique_filename(os.path.join(directory, new_name))

    os.rename(path, new_path)
    print(f"File {path} renamed to {new_name}.")

def main():
    parser = argparse.ArgumentParser(description='Split a markdown file at each line containing only "* * *" and rename it based on its first section and creation time.')
    parser.add_argument('input_filename', type=str, help='The markdown file to split and rename.')

    args = parser.parse_args()
    split_markdown_file(args.input_filename)

if __name__ == "__main__":
    main()
