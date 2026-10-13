import speech_recognition as sr
from gtts import gTTS
import os
import uuid

# Folder for all mp3 files
AUDIO_DIR = "audio_files"
os.makedirs(AUDIO_DIR, exist_ok=True)

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
    try:
        return r.recognize_google(audio)
    except:
        return None

def speak(text):
    # Use UUID for unique filenames
    filename = os.path.join(AUDIO_DIR, f"{uuid.uuid4()}.mp3")
    tts = gTTS(text)
    tts.save(filename)
    return filename
