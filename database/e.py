import json

add = {
    "bg_color" : None,
    "text_color" : None,
    "text_footer" : None,
    "bg_image" : None
}

with open("db.json", 'r') as f:
    data = json.load(f)

for i in data:
    i['settings'].pop("welcometext")
    i['welcome'] = add
    
with open("db.json", 'w') as f:
    json.dump(data, f, indent=4)