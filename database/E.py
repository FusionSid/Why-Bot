import json

with open('db.json', 'r') as f:
  data = json.load(f)
for i in data:
  i['settings']['plugins']['Fun'] = True
with open('db.json', 'w') as f:
  json.dump(data, f, indent=4)