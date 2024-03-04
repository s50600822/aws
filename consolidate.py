import json
from datetime import datetime
from collections import defaultdict
from pathlib import Path  # Import Path from pathlib

def extract_timestamp_from_filename(filename):
    # Extract timestamp from the filename (e.g., 231110051045)
    timestamp_str = filename[:12]
    timestamp = datetime.strptime(timestamp_str, "%y%m%d%H%M%S")
    return timestamp

def find_earliest_timestamp(files):
    url_timestamps = defaultdict(lambda: datetime.max)
    for file in files:
        with open(file, 'r') as f:
            data = json.load(f)
            timestamp = extract_timestamp_from_filename(file.name)
            for url in data:
                url_timestamps[url] = min(url_timestamps[url], timestamp)
    return url_timestamps

def invert_and_sort_dict(original_dict):
    inverted_dict = {}
    for key, value in sorted(original_dict.items()):
        if value in inverted_dict:
            inverted_dict[value].append(key)
        else:
            inverted_dict[value] = [key]
    return inverted_dict

def main():
    directory = "./"  # Change this to the directory containing your files
    files = [file for file in Path(directory).iterdir() if file.is_file() and file.name.endswith('.json')]

    url_timestamps = find_earliest_timestamp(files)
    timestamp_urls = invert_and_sort_dict(url_timestamps)
    count = 1
    for value, keys in sorted(timestamp_urls.items()):
        print(f"\n## {value}\n")
        for key in keys:
            print(f"{count}. [{key}]({key})")
            count += 1
        print("---")
    # current_date = None
    # count = 1
    # for url, timestamp in url_timestamps.items():
    #     date_str = timestamp.strftime("%Y-%m-%d")
    #     if date_str != current_date:
    #         if current_date is not None:
    #             print("---")
    #         print(f"\nAdded on {date_str}:")
    #         current_date = date_str
    #     print(f"{count} ![Image {len(url_timestamps)}]({url})")
    #     count = count+1

if __name__ == "__main__":
    main()
