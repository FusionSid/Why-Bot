import json

with open("db.json") as f:
    data = json.load(f)

for k,v in data.items():
    role = v["autorole"]["bot"]
    role2 = v["autorole"]["all"]

    if role is not None:
        v["autorole"]["bot"] = [role]
    else:
        v["autorole"]["bot"]

    if role2 is not None:
        v["autorole"]["all"] = [role2]
    else:
        v["autorole"]["all"]

for k, v in data.items():
    text = v['settings']['plugins']['TextConvert']
    v['settings']['plugins'].pop("TextConvert")
    v['settings']['plugins']['Text'] = text

with open('db.json', 'w') as f:
    json.dump(data, f, indent=4)