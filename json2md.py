#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import argparse
from datetime import datetime
import re
import os
from typing import List, Dict, Tuple, Optional

def validate_json(data: List[Dict]) -> None:
    """
    Validate the structure of the provided JSON data.

    Args:
        data (List[Dict]): A list of dictionaries representing conversations.

    Raises:
        ValueError: If the root element is not a list or if any conversation dictionary
                    does not contain a 'mapping' key.

    This function checks if the root of the JSON is a list and if each item in the list
    is a dictionary with a required 'mapping' key. If these conditions are not met,
    a ValueError with a descriptive message is raised.
    """
    if not isinstance(data, list):
        raise ValueError("Root JSON element should be a list of conversations.")
    for conversation in data:
        if not isinstance(conversation, dict) or 'mapping' not in conversation:
            raise ValueError("Each conversation should be a dictionary with a 'mapping' key.")

def sanitize_filename(title: str) -> str:
    """
    Sanitize a title string to create a valid and safe filename.

    Args:
        title (str): The original title string that needs to be sanitized.

    Returns:
        str: A sanitized string safe for use as a filename.

    The function removes any characters that are not alphanumeric, spaces, or
    specific punctuation, and then replaces spaces and punctuation with underscores
    to ensure a valid filename format that is also filesystem-safe.
    """
    #sanitized_title = re.sub('[^a-zA-Z0-9 \n.,:;/]', '', title)
    sanitized_title = re.sub('[^a-zA-Z0-9\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FAF \n.,:;/]', '', title) # Japanese
    sanitized_title = re.sub(r"[ .,:;/]+", "_", sanitized_title).rstrip("_")
    return sanitized_title

def format_message(message: Dict) -> str:
    """
    Format a message dictionary into a Markdown formatted string.

    Args:
        message (Dict): A dictionary containing the message details.

    Returns:
        str: A formatted string in Markdown that represents the message.

    This function extracts the author and content from the message dictionary
    and formats it into a Markdown heading and content section.
    """
    if message["author"]["role"] == "user":
        author = "User" 
    else:
        author = "Assistant"
    if 'metadata' in message and 'model_slug' in message['metadata']:
        author += f" ({message['metadata']['model_slug']})"
    content = message["content"]["parts"][0]  # Assuming single part content for simplicity
    return f"## {author}\n\n{content}\n\n"

def format_datetime(timestamp: Optional[int]) -> str:
    """
    Convert a UNIX timestamp into a human-readable date and time string.

    Args:
        timestamp (Optional[int]): UNIX timestamp.

    Returns:
        str: A string representing the formatted date and time.

    If the timestamp is not provided (None), the function returns ''.
    """
    return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S') if timestamp else ""

def format_datetime_for_filename(timestamp: Optional[int]) -> str:
    """
    Convert a UNIX timestamp into a string format suitable for use in filenames.

    Args:
        timestamp (Optional[int]): UNIX timestamp.

    Returns:
        str: A string representing the date suitable for filenames.

    The function formats the timestamp specifically for inclusion in filenames,
    avoiding characters that might not be suitable such as colons or spaces.
    """
    return datetime.fromtimestamp(timestamp).strftime('%Y_%m%d') if timestamp else ""

def generate_frontmatter(conversation: Dict) -> str:
    """
    Generate the Markdown frontmatter for a conversation.

    Args:
        conversation (Dict): A dictionary representing the conversation.

    Returns:
        str: The frontmatter for the Markdown document.
    """
    title = conversation['title']
    return (
        f"---\ntitle: {title}\ncreate_time: {format_datetime(conversation['create_time'])}\n"
        f"update_time: {format_datetime(conversation['update_time'])}\n"
        f"conversation_id: {conversation['conversation_id']}\n---\n\n"
    )

def compose_markdown_document(conversation: Dict) -> Tuple[str, str]:
    """
    Generate the Markdown content and a filename timestamp from a conversation dictionary.

    Args:
        conversation (Dict): A dictionary representing the conversation.

    Returns:
        Tuple[str, str]: A tuple containing the complete Markdown content as a string and a creation
                         time string formatted for filenames.

    This function constructs the Markdown representation of the conversation, including
    frontmatter with metadata and formatted messages.
    """
    title = conversation['title']
    create_time = format_datetime_for_filename(conversation['create_time'])
    frontmatter = generate_frontmatter(conversation)
    messages_content = f"# {title}\n\nCreation Time: {format_datetime(conversation['create_time'])}\n\nUpdate Time: {format_datetime(conversation['update_time'])}\n\n"
    for _, details in conversation['mapping'].items():
        if details['message'] and details['message']['content']['content_type'] == 'text':
            messages_content += format_message(details['message'])
    return frontmatter + messages_content, create_time

def save_markdown(filepath: str, content: str) -> None:
    """
    Write the generated Markdown content to a specified file.

    Args:
        filepath (str): The full path where the file will be written.
        content (str): The Markdown content to be written.

    This function opens the specified file path in write mode, writes the content,
    and then safely closes the file, ensuring data integrity even if an error occurs.
    """
    with open(filepath, 'w', encoding='utf-8') as file:
        file.write(content)
    print(f"Created: {filepath}")

def generate_markdown_files_from_json(json_filename: str, output_dir: str) -> None:
    """
    Process a JSON file to generate Markdown files for each conversation.

    Args:
        json_filename (str): Path to the JSON file containing conversation data.
        output_dir (str): Directory where the Markdown files will be saved.

    This function reads a JSON file, validates and processes each conversation to generate
    Markdown files, which are then saved to the specified output directory.
    """
    try:
        with open(json_filename, 'r', encoding='utf-8') as json_file:
            conversations = json.load(json_file)
        validate_json(conversations)
        for conversation in conversations:
            content, create_time = compose_markdown_document(conversation)
            filename = sanitize_filename(conversation['title']) + f"_{create_time}.md"
            filepath = os.path.join(output_dir, filename)
            save_markdown(filepath, content)
    except FileNotFoundError:
        print(f"Error: The file {json_filename} was not found.")
    except json.JSONDecodeError:
        print(f"Error: There was an issue decoding {json_filename}. Please check the file format.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def main() -> None:
    """
    Main function to handle command-line execution for processing JSON to Markdown.

    This function parses command-line arguments for the JSON filename and output directory,
    and calls the function to process the JSON file into Markdown.
    """
    parser = argparse.ArgumentParser(description='Process JSON conversations into markdown files.')
    parser.add_argument('json_filename', help='The JSON file containing the conversations.')
    parser.add_argument('-o', '--output', default='.', help='Directory to save the markdown files (default is current directory).')
    args = parser.parse_args()

    generate_markdown_files_from_json(args.json_filename, args.output)

if __name__ == "__main__":
    main()
