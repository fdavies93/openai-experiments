import openai
import pyaudio
import wave
import requests
import os
from pynput import keyboard
from playsound import playsound
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_KEY")
eleven_api_key = os.getenv("ELEVEN_LABS_KEY")

recording = False

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
WAVE_OUTPUT = "./last-audio.wav"

audio = pyaudio.PyAudio()
stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
cur_frames = []
recording = False
transcript = ""
new_transcript = False


def synthesise(text, voice):
    voices = {
        'bella': 'EXAVITQu4vr4xnSDxMaL',
        'elli': 'MF3mGyEYCl7XYWbV9V6O',
        'domi': 'AZnzlk1XvdvUeBnXmlld',
        'rachel': '21m00Tcm4TlvDq8ikWAM'
    }
    headers = {
        "xi-api-key": eleven_api_key
    }
    body = {
        "text": text,
        "voice_settings": {
            "stability": 0,
            "similarity_boost": 0
        }
    }
    res = requests.post("https://api.elevenlabs.io/v1/text-to-speech/"+voices.get(voice),json=body,headers=headers)
    return res


def ask_question(msgs):
    return openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=msgs
    )

def extract_reply(res):
    return res['choices'][0]['message']

def on_press(key : keyboard.Key):
    if keyboard.Key.ctrl == key:
        global recording
        recording = True

def on_release(key : keyboard.Key):
    if keyboard.Key.ctrl == key:
        global recording
        recording = False
    
    global cur_frames
    with wave.open(WAVE_OUTPUT, "wb") as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(audio.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(cur_frames))
    cur_frames = []
    audio_file = open(WAVE_OUTPUT, "rb")
    global transcript
    transcript = openai.Audio.transcribe("whisper-1", audio_file)["text"]
    global new_transcript
    new_transcript = True

cur_messages = [
        {"role": "system", "content": "You are a helpful assistant. You are having a spoken conversation. Please keep your responses brief as appropriate for a spoken conversation."}
    ]
user_in = ""
print("ChatGPT Speech Test")

listener = keyboard.Listener(on_press=on_press, on_release=on_release)
listener.start()

while True:
    if recording:
        cur_frames.append(stream.read(CHUNK))
    if new_transcript:
        new_transcript = False
        print("YOU: " + transcript)
        cur_messages.append({"role": "user", "content": transcript})
        res = ask_question(cur_messages)
        reply = extract_reply(res)
        print("GPT: " + reply["content"])
        voice = synthesise(reply["content"],'elli')
        with open("last_response.mp3","wb") as f:
            f.write(voice.content)
        playsound("last_response.mp3")
        cur_messages.append(reply)