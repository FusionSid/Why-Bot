import json

with open("db.json") as f:
    data = json.load(f)

with open("db_backup", 'w') as f:
    json.dump(data, f, indent=4)

new_data = {}

for i in data:
    new_data[i['guild_id']] = i
    
with open("db.json", 'w') as f:
    json.dump(new_data, f, indent=4)