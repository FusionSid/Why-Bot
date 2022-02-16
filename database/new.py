import json

with open("userdb.json") as f:
    data = json.load(f)

new_data = {

}

for i in data:
    new_data[i['user_id']] = i
    new_data[i['user_id']]["on_pinged_toggled"] = True

with open("userdb.json", 'w') as f:
    json.dump(data,f, indent=4)