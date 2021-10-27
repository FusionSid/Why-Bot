import json

name = "Siddhesh"
pname = "sus"

with open('customplaylist.json') as f:
    data = json.load(f)
print(data)
if name in data:
    print(name)