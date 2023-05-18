#!/usr/bin/env python3
import json
from itertools import groupby
import argparse

# Create the parser
parser = argparse.ArgumentParser(description='Merge two JSON files, remove duplicates, and sort by "Time" in reverse order.')

# Add the arguments
parser.add_argument('file1', type=str, help='The first JSON file to merge')
parser.add_argument('file2', type=str, help='The second JSON file to merge')
parser.add_argument('-o', '--output', type=str, default='merged.json', help='The output JSON file (default: merged.json)')


# Parse the command-line arguments
args = parser.parse_args()

# Load the first JSON file
with open(args.file1) as f:
    data1 = json.load(f)

# Load the second JSON file
with open(args.file2) as f:
    data2 = json.load(f)

# Combine the two data lists
combined_data = data1 + data2

# Sort by the dictionaries converted to JSON strings to group duplicates
combined_data.sort(key=json.dumps)

# Remove duplicates
merged_data = [next(g) for k, g in groupby(combined_data, json.dumps)]

# Write the merged data to a new JSON file
with open(args.output, 'w') as f:
    json.dump(merged_data, f, indent=2)

print(f'Merged data has been written to {args.output}')