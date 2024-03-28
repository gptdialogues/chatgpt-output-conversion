#!/usr/bin/env python3
import json
import argparse
from datetime import datetime
import re
import os

def validate_json(data):
    """Validates the structure of the provided JSON data."""
    if not isinstance(data, list):
        raise ValueError("Root JSON element should be a list of documents.")

    for document in data:
        if not isinstance(document, dict) or 'messages' not in document:
            raise ValueError("Each document should be a dictionary with a 'messages' key.")

        for message in document['messages']:
            if not isinstance(message, dict) or 'role' not in message:
                raise ValueError("Each message should be a dictionary with a 'role' key.")

def json_to_markdown(json_data):
    markdown = ""

    for document in json_data:
        title = document.get('title', 'Default Title')
        markdown += f"# {title}\n\n"
        if 'create_time' in document:
            dt_object = datetime.fromtimestamp(document['create_time'])
            markdown += f"Creation Time: {dt_object}\n\n"
        for message in document['messages']:
            markdown += f"## {message['role'].title()}\n\n"
            if 'create_time' in message:
                try:
                    # Attempt to convert the timestamp to a datetime object
                    dt_object = datetime.fromtimestamp(message['create_time'])
                    markdown += f"Time: {dt_object}\n\n"
                except TypeError:
                    # Handle the case where 'create_time' is None or not valid
                    markdown += "Time: Invalid or missing timestamp\n\n"
            content = message.get('content')
            if content:
                for item in content:
                    if isinstance(item, str):
                        markdown += f"{item}\n\n"
                    elif isinstance(item, dict):
                        content_type = item.get('content_type')
                        if content_type == 'image_asset_pointer':
                            markdown += f"Image Asset: {item.get('asset_pointer')}\n"
                            markdown += f"Size: {item.get('size_bytes')} bytes\n"
                            markdown += f"Dimensions: {item.get('width')}x{item.get('height')}\n\n"
            if message.get('model'):
                markdown += f"Model: {message['model']}\n\n"
        markdown += f"* * *\n\n"
    return markdown

def split_markdown_file(contents, output_base_name, remove_input=False):
    parts = re.split(r'\n\* \* \*\n', contents)

    for i, part in enumerate(parts):
        part = part.strip()
        if part:
            output_filename = f"{output_base_name}_part{i}.md"
            output_filename = get_unique_filename(output_filename)
            with open(output_filename, 'w') as file:
                file.write(part)
            rename_file(output_filename)

    if remove_input:
        os.remove(input_filename)
        print(f"Input file {input_filename} removed.")

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
    parser = argparse.ArgumentParser(description='Convert JSON to Markdown, split the markdown file, and rename it based on its content.')
    parser.add_argument('filename', help='The name of the json file')
    parser.add_argument('--remove-input', action='store_true', help='Remove the input file after processing.')
    args = parser.parse_args()

    try:
        with open(args.filename, 'r') as json_file:
            data = json.load(json_file)
        validate_json(data)
        markdown = json_to_markdown(data)
        output_base_name = args.filename.split('.')[0]
        split_markdown_file(markdown, output_base_name, args.remove_input)
    except json.decoder.JSONDecodeError:
        print("Error: Malformed JSON input.")
    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
