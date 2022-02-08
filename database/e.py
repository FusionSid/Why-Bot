import json

guilds = []

with open("db.json", 'r') as f:
    data = json.load(f)

with open("dbbackup.json", 'w') as f:
    json.dump(data, f, indent=4)

for i in data:
    if i['guild_id'] in guilds:
        data.remove(i)
        print("1")
        
    else:
        print("2")
        guilds.append(i['guild_id'])
with open("db.json", 'w') as f:
    json.dump(data, f, indent=4)