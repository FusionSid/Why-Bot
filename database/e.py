import json

with open("db.json") as f:
  data = json.load(f)

for i in data:
  try:
    lol = i["settings"]['plugins']
  except KeyError:
    i['settings'] ={
            "welcometext": "THANK YOU FOR JOINING. HOPE YOU WILL ENJOY YOUR STAY",
            "autocalc":True,
            "plugins": {
                "Counting": True,
                "Moderation": True,
                "Economy": True,
                "TextConvert": True,
                "Search": True,
                "Welcome": True,
                "Leveling": True,
                "Music": True,
                "Onping": True,
                "Ticket": True,
                "Minecraft": True,
                "Utilities": True,
                "Fun": True
            }
            },

with open("db.json", 'w') as f:
  json.dump(data, f, indent=4)