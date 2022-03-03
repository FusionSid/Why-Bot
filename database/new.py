import json

with open("db.json") as f:
    data = json.load(f)

for k, v in data.items():
    v['settings']['plugins']['Logging'] = False

with open('db.json', 'w') as f:
    json.dump(data, f, indent=4)