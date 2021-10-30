import pyttsx3
import os

s = pyttsx3.init()

e = "HI"
s.save_to_file(e, 'test.mp3')
s.runAndWait()

os.remove('test.mp3')