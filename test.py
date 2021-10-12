import os
import json

def startguildsetup(id):
  cd = os.getcwd()
  os.chdir("{}/Setup".format(cd))
  file = [
    {"mod_channel": None},
    {"counting_channel": None},
    {"welcome_channel": None},
    {"prefix": None}
  ]
  with open(f'{id}.json', 'w') as f:
    json.dump(file, f)
  os.chdir(cd)

startguildsetup(123)

with open('w.json', 'w') as f:
    print('e')
