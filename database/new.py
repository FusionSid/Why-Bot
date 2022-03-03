import json

with open("db.json") as f:
    data = json.load(f)

for k, v in data.items():
    if  v['autorole']["all"] is None:
        v['autorole']["all"] = []
    if  v['autorole']["bot"] is None:
        v['autorole']["bot"] = []

with open('db.json', 'w') as f:
    json.dump(data, f, indent=4)