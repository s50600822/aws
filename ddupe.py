import os
import json
from collections import defaultdict
from datetime import datetime

# Function to parse the filename and extract timestamp
def parse_filename(filename):
    timestamp_str = os.path.splitext(filename)[0]
    return datetime.strptime(timestamp_str, "%y%m%d%H%M%S")

# Function to load JSON file
def load_json(filepath):
    with open(filepath, 'r') as f:
        return json.load(f)

# Function to save JSON file
def save_json(filepath, data):
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=4)

# Function to find duplicate JSON files and keep the one with earliest timestamp
def remove_duplicates(directory):
    file_dict = defaultdict(list)

    # Collecting files and grouping by content
    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            filepath = os.path.join(directory, filename)
            timestamp = parse_filename(filename)
            content = load_json(filepath)
            file_dict[json.dumps(content)].append((filename, timestamp))

    # Deleting duplicate files
    for content, files in file_dict.items():
        if len(files) > 1:
            files.sort(key=lambda x: x[1])  # Sorting by timestamp
            for filename, _ in files[1:]:
                print("Deleting {} in favor of {}".format(filename, files[0][0]))
                os.remove(os.path.join(directory, filename))

directory = './'

remove_duplicates(directory)
