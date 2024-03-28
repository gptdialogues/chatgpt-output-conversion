# ChatGPT Output Conversion Tool

This repository contains a script for processing and converting downloaded ChatGPT outputs. The goal is to enable efficient and streamlined conversion of ChatGPT outputs from JSON to individual Markdown files, renaming them based on their titles and creation dates.

## Workflow

1. Download ChatGPT output as JSON using "backup.js" from [ChatGPT Backup Repository](https://github.com/abacaj/chatgpt-backup).
2. Convert the JSON file into individual Markdown files using `json2md.py`, which will also rename the files based on the titles of ChatGPT discourse and their creation dates.

## How to Use

### Prerequisites

You need to have Python installed on your machine to run this script.

### Steps

1. Clone this repository:
    ```sh
    git clone https://github.com/gptdialogues/chatgpt-output-conversion.git
    ```
2. Change directory to the cloned repository:
    ```sh
    cd chatgpt-output-conversion
    ```
3. Use `backup.js` to download your ChatGPT output as a JSON file. More instructions can be found in the [ChatGPT Backup Repository](https://github.com/abacaj/chatgpt-backup).
4. Convert the JSON file to individual Markdown files and rename them:
    ```sh
    python json2md.py <filename> [--remove-input]
    ```
    - `filename`: Filename of the input JSON file
    - `--remove-input`: (Optional) Removes the input JSON file after processing

The `json2md.py` script will split the converted Markdown content into individual files based on the distinct discourses in the original JSON file. Each file will be renamed to include the title of the discourse and its creation date for easy identification.

## Contributing

Feel free to fork the project and submit a pull request with your changes!

## License

This project is licensed under the terms of the MIT License.
