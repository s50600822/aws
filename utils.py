import requests
import re
import json
import os

from datetime import datetime

def create_markdown_file(file_name, url_list):
    with open(file_name, 'w') as file:
        file.write("# List of Images\n\n")
        for i, url in enumerate(url_list, 1):
            file.write(f"{i}. ![Image {i}]({url})\n")

def save_to_json(data):
    timestamp = datetime.now().strftime("%y%m%d%H%M%S")
    filename = f"{timestamp}.json"

    with open(filename, 'w') as json_file:
        json.dump(data, json_file, indent=2)

    print(f"Data saved to {filename}")

def extract(page, more, l):
    url = "https://www.credly.com/organizations/amazon-web-services/badges?page={}"
    print(url.format(page))
    response = requests.get(url.format(page))
    if response.status_code == 200:
        url_pattern = re.compile(r'https://images\.credly\.com/images/[a-f0-9-]+/image\.png')

        matches = url_pattern.findall(response.text)
        print(len(matches))
        for match in matches:
            l.append(match)
        if None == matches or len(matches) == 0:
            print("last page {}".format(page-1))
            return False
        return True
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        more = False


def load_last_json():
    json_files = [f for f in os.listdir() if f.endswith(".json")]
    json_files.sort(key=lambda x: os.path.getmtime(x), reverse=True)
    if json_files:
        latest_json_file = json_files[0]
        with open(latest_json_file, 'r') as json_file:
            data = json.load(json_file)

        return data
    else:
        print("No JSON files found.")
        return None
