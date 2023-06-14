#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
import subprocess
import sys
import re
import os
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(description='Convert a markdown file using pandoc, then replace some strings with sed.')
    parser.add_argument('input_file', type=str, help='The markdown file to be converted.')
    parser.add_argument('-o', '--output_file', nargs='?', const=True, default=False, help='Specify the output filename. If not specified, the result will be printed to stdout.')
    args = parser.parse_args()

    pandoc_command = ['pandoc', '-s', args.input_file, '--mathjax', '--shift-heading-level-by=-1']
    pandoc_process = subprocess.Popen(pandoc_command, stdout=subprocess.PIPE)

    pandoc_output, _ = pandoc_process.communicate()

    output = re.sub(r'text-rendering: optimizeLegibility;', 
                    r'text-rendering: optimizeLegibility;\n      font-family: Arial, sans-serif;', 
                    pandoc_output.decode('utf-8'))

    if args.output_file is False: # No -o argument provided, print to stdout
        sys.stdout.write(output)
    else: 
        if args.output_file is True: # -o argument provided, but no filename specified
            output_file = Path(args.input_file).stem + '.html'
        else: # -o argument provided, and a filename specified
            output_file = args.output_file
        
        if os.path.exists(output_file):
            overwrite = input(f"File {output_file} already exists. Do you want to overwrite it? (yes/no): ")
            if overwrite.lower() != 'yes':
                print('Aborted.')
                return

        with open(output_file, 'w') as f:
            f.write(output)

if __name__ == "__main__":
    main()
