#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
import os
import re
from datetime import datetime

def get_new_name(path):
    with open(path, 'r') as file:
        lines = file.readlines()

    first_section = ""
    creation_time = ""
    for line in lines:
        if line.startswith('# '):
            first_section = line[2:].strip()
            first_section = first_section.replace("'", "") # Remove single quote
            first_section = first_section.replace('"', "") # Remove double quote
            first_section = re.sub(r"[ .,:;/]", "_", first_section) # Replace space, period, comma, semicolon, colon with underbar
            first_section = first_section.replace("__", "_") # Replace double underbar with single underbar
            first_section = first_section.rstrip("_") # Remove trailing underbar
        if line.startswith('Creation Time:'):
            creation_time = line[len('Creation Time:'):].strip().split()[0] # We only take the date part
            creation_time = datetime.strptime(creation_time, '%Y-%m-%d')
            creation_time = creation_time.strftime('%Y_%m%d')
        if first_section and creation_time:
            break

    return f'{first_section}_{creation_time}.md' if first_section and creation_time else None

def rename_files(args):
    for path in args.files:
        if not os.path.exists(path):
            print(f"File {path} does not exist.")
            continue

        new_name = get_new_name(path)
        if not new_name:
            print(f"Could not determine new name for file {path}.")
            continue

        directory = os.path.dirname(path)
        new_path = os.path.join(directory, new_name)

        os.rename(path, new_path)
        print(f"File {path} renamed to {new_name}.")

def main():
    parser = argparse.ArgumentParser(description='Rename markdown file based on its first section and creation time.')
    parser.add_argument('files', nargs='*', type=str, help='The path of the markdown file(s) to rename.')

    args = parser.parse_args()

    rename_files(args)

if __name__ == "__main__":
    main()
