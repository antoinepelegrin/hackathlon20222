from playsound import playsound
from gtts import gTTS
import os
import time

#greetings
def play(cmd):

   #if os.path.exists('audio.mp3'):
   #   os.remove('audio.mp3')

   tts = gTTS(text=cmd, lang='en' , 
   slow=False)
   tts.save('audio.mp3')

   playsound('audio.mp3')

   os.remove('audio.mp3')
   
