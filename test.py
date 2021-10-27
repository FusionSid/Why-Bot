import json

name = "Siddhesh"
pname = "sus"

with open('customplaylist.json') as f:
    data = json.load(f)
if name in data:
    data[name][pname] = []
else:
    plist = {pname:[]}
    data[name] = plist
with open('customplaylist.json', 'w') as f:
    json.dump(data, f)