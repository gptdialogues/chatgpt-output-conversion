# ChatGPT Output Conversion Tool

This repository contains a script for processing and converting downloaded ChatGPT outputs. The goal is to enable efficient and streamlined conversion of ChatGPT outputs from JSON to individual Markdown files.

## Workflow

1. Export `conversations.json` containing ChatGPT history
2. Convert the JSON file into individual Markdown files using `json2md.py`

## Usage

### 1. `json2md.py`

`json2md.py` processes JSON files containing conversation data, validating and converting each conversation into a Markdown formatted document.

```bash
python3 json2md.py <json_filename> [-o <output_file>]
```

- `<json_filename>`: The JSON file containing the conversation data.
- `<output_file>`: (Optional) The directory where Markdown files will be saved; defaults to the current directory with summarized titles given by ChatGPT.

### 2. `merge_json.py`

`merge_json.py` merges two JSON files into one, ensuring that there are no duplicates and that the contents are sorted by timestamp in reverse order. This is useful for consolidating conversation logs or similar data.

```bash
python3 merge_json.py <file1> <file2> [-o <output_file>]
```
- `<file1>` and `<file2>`: The JSON files to be merged.
- `<output_file>`: (Optional) The name of the output file to store the merged JSON; defaults to `merged.json`.

* * *

## How to Download Your ChatGPT Conversational Data

Before using `json2md.py`, you may need to download your ChatGPT conversation history. Follow these steps to download your data from OpenAI:

1. **Sign in**: Access ChatGPT at [https://chat.openai.com](https://chat.openai.com) and sign in.
2. **Navigate to Settings**: Click on the settings option at the bottom left of the page.
3. **Data Controls**: Select 'Data Controls' and then click on 'Export Data'.
4. **Confirm Export**: Click 'Export', and then in the confirmation modal, click 'Confirm Export'.
5. **Download Data**: You will receive an email with a link to download your data. This link expires after 24 hours.
6. **File Format**: The download will be a .zip file containing your conversation history in `conversations.json` and other data.

For more detailed instructions and screenshots, please refer to the official guide on [How to Export ChatGPT History and Data](https://help.openai.com/en/articles/7260999-how-do-i-export-my-chatgpt-history-and-data).

