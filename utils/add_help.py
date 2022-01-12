import json

with open("database/help.json") as f:
    data = json.load(f)
    

name = input("Name: ")

for cmd in data:
    if cmd['name'] == name:
        print("already exists")

desc = input("Description: ")


use = input("Usage: ")

cat = input("Category: ")

help_command = {
    "name": name,
    "description": desc,
    "usage": f"`{use}`",
    "category":cat
}

data.append(help_command)
with open('database/help.json', 'w') as f:
    json.dump(data, f, indent=4)