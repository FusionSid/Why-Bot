import json

with open("db.json") as f:
    data = json.load(f)

with open('db.json', 'w') as f:
    json.dump(data, f, indent=4)