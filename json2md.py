#!/usr/bin/env python3
import json
import argparse
import datetime

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
            dt_object = datetime.datetime.fromtimestamp(document['create_time'])
            markdown += f"Creation Time: {dt_object}\n\n"
        for message in document['messages']:
            markdown += f"## {message['role'].title()}\n\n"
            if 'create_time' in message:
                dt_object = datetime.datetime.fromtimestamp(message['create_time'])
                markdown += f"Time: {dt_object}\n\n"
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

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', help='The name of the json file')
    args = parser.parse_args()

    try:
        with open(args.filename, 'r') as json_file:
            data = json.load(json_file)
        validate_json(data)
        markdown = json_to_markdown(data)
        print(markdown)
    except json.decoder.JSONDecodeError:
        print("Error: Malformed JSON input.")
    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
