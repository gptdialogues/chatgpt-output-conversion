#!/usr/bin/env python3
import json
import argparse
import datetime

def json_to_markdown(json_data):
    markdown = ""

    for document in json_data:
        markdown += f"# {document['title']}\n\n"
        dt_object = datetime.datetime.fromtimestamp(document['create_time'])
        markdown += f"Creation Time: {dt_object}\n\n"
        for message in document['messages']:
            markdown += f"## {message['role'].title()}\n\n"
            if 'create_time' in message:
                dt_object = datetime.datetime.fromtimestamp(message['create_time'])
                markdown += f"Time: {dt_object}\n\n"
            if 'content' in message:
                markdown += f"{' '.join(message['content'])}\n\n"
            if message.get('model'):
                markdown += f"Model: {message['model']}\n\n"
        markdown += f"* * *\n\n"
    return markdown

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', help='The name of the json file')
    args = parser.parse_args()

    with open(args.filename, 'r') as json_file:
        data = json.load(json_file)

    markdown = json_to_markdown(data)
    print(markdown)

if __name__ == "__main__":
    main()
