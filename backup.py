from threading import Thread
import os
import time

def run():
  while True:
    os.system("git add .")
    os.system("git commit -m 'backup'")
    os.system("git push")
    time.sleep(3600)

def backup():
  t = Thread(target=run)
  t.start()
