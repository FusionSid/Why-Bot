import json

with open("db.json") as f:
    data = json.load(f)

new_data = {}

for i in data:
    new_data[i['guild_id']] = i
    
with open("db.json", 'w') as f:
    json.dump(new_data, f, indent=4)