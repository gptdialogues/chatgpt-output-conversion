# ChatGPT Output Conversion Tool

This repository contains a collection of scripts for processing and converting downloaded ChatGPT outputs. The goal is to enable efficient and streamlined conversion of ChatGPT outputs from JSON to Markdown files and rename them based on their titles.

## Workflow

1. Download ChatGPT output as JSON using "backup.js" from [ChatGPT Backup Repository](https://github.com/abacaj/chatgpt-backup)
2. Merge individual JSON files into a single JSON file using `merge_json.py` (if you have multiple JSON files to combine)
3. Convert the merged JSON file into a Markdown file using `json2md.py`
4. Split the merged Markdown file into individual files using `split_md.py`
5. Rename each split file using `rename_divided_files.py` based on the titles of ChatGPT discourse.

## How to Use

### Prerequisites

You need to have Python installed on your machine to run these scripts. 

### Steps

1. Clone this repository:
    ```sh
    git clone https://github.com/gptdialogues/chatgpt_output_conversion.git
    ```
2. Change directory to the cloned repository:
    ```sh
    cd chatgpt_output_conversion
    ```
3. Use `backup.js` to download your ChatGPT output as JSON file(s). More instructions can be found in the [ChatGPT Backup Repository](https://github.com/abacaj/chatgpt-backup).
4. If you have multiple JSON files, you can merge them into one file:
    ```sh
    python merge_json.py <file1> <file2> -o <output_file>
    ```
    - `file1`: The first JSON file to merge
    - `file2`: The second JSON file to merge
    - `output_file`: Filename of the merged JSON file (default: merged.json)
5. Convert the JSON file to Markdown:
    ```sh
    python json2md.py <filename>
    ```
    - `filename`: Filename of the input JSON file
6. Split the merged Markdown file into individual files:
    ```sh
    python split_md.py <input_filename>
    ```
    - `input_filename`: Filename of the input Markdown file
7. Rename each split file based on their ChatGPT discourse titles:
    ```sh
    python rename_divided_files.py <file>
    ```
    - `file`: The path of the markdown file to rename

Please note that each script takes the output of the previous script as its input. Therefore, you should run these scripts in the specified order.

## Contributing

Feel free to fork the project and submit a pull request with your changes!
