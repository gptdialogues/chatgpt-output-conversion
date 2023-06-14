#!/usr/bin/env python3

import argparse
import subprocess
import sys
import re

def main():
    parser = argparse.ArgumentParser(description='Convert a markdown file using pandoc, then replace some strings with sed.')
    parser.add_argument('input_file', type=str, help='The markdown file to be converted.')
    parser.add_argument('-o', '--output_file', type=str, default=None, help='Specify the output filename. If not specified, the result will be printed to stdout.')
    args = parser.parse_args()

    pandoc_command = ['pandoc', '-s', args.input_file, '--mathjax', '--shift-heading-level-by=-1']
    pandoc_process = subprocess.Popen(pandoc_command, stdout=subprocess.PIPE)

    pandoc_output, _ = pandoc_process.communicate()

    output = re.sub(r'text-rendering: optimizeLegibility;', 
                    r'text-rendering: optimizeLegibility;\nfont-family: Arial, sans-serif;', 
                    pandoc_output.decode('utf-8'))

    if args.output_file is None:
        sys.stdout.write(output)
    else:
        with open(args.output_file, 'w') as f:
            f.write(output)

if __name__ == "__main__":
    main()
