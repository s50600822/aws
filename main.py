from utils import create_markdown_file, save_to_json, extract, load_last_json

page = 0
more = True
l = []

while more:
    page += 1
    more = extract(page, more, l)

s = sorted(set(l))
print(len(s))

prev = load_last_json()
if prev and prev == s:
    print("NO NEW CRED ADDED")
else:
    save_to_json(s)

file_name = "Readme.md"
create_markdown_file(file_name, s)
print(" {} created successfully.".format(file_name))
