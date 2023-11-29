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

def main():
    directory = "./"  # Change this to the directory containing your files
    files = [file for file in Path(directory).iterdir() if file.is_file() and file.name.endswith('.json')]

    url_timestamps = find_earliest_timestamp(files)

    for url, timestamp in url_timestamps.items():
        print(f"URL: {url}, Added on: {timestamp}")

if __name__ == "__main__":
    main()
