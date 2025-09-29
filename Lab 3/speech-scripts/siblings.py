#!/usr/bin/env -S /home/pi/INFO-5345/Lab\ 3/.venv/bin/python
# This script was developed with assistance from OpenAI's ChatGPT.

import sys
import time
import queue
import subprocess
import sounddevice as sd
from vosk import Model, KaldiRecognizer
import json

q = queue.Queue()

# --- Speak using espeak ---
def speak(text):
    subprocess.run(
        ["espeak", "-ven+f2", "-k5", "-s150", text],
        check=False
    )

def callback(indata, frames, time_, status):
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))

# --- Map words to numbers ---
word_to_num = {
    "zero": "0", "one": "1", "two": "2", "three": "3",
    "four": "4", "five": "5", "six": "6", "seven": "7",
    "eight": "8", "nine": "9", "ten": "10"
}

# --- Step 0: Check microphone ---
devices = sd.query_devices()
inputs = [d for d in devices if d["max_input_channels"] > 0]
if not inputs:
    print("ERROR: No input microphone detected.")
    speak("No microphone detected. Please connect one and try again.")
    sys.exit(1)
else:
    print("Input devices found:")
    for idx, d in enumerate(inputs):
        print(f"  {idx}: {d['name']}")

# --- Step 1: Ask question ---
speak("How many siblings do you have? Please answer with a number.")
time.sleep(2)

# --- Step 2: Setup recognizer ---
model = Model(lang="en-us")
device_info = sd.query_devices(None, "input")
samplerate = int(device_info["default_samplerate"])
rec = KaldiRecognizer(model, samplerate)

# --- Step 3: Listen until number is found or timeout ---
timeout = time.time() + 12  # 12s listening window
number = None

with sd.RawInputStream(samplerate=samplerate, blocksize=8000,
                       dtype="int16", channels=1, callback=callback):
    print("Listening... say a number.")
    while time.time() < timeout and not number:
        data = q.get()
        if rec.AcceptWaveform(data):
            result = json.loads(rec.Result())
            print("DEBUG Final:", result)  # full phrase
            if "text" in result and result["text"]:
                words = result["text"].split()
                for w in words:
                    if w.isdigit():
                        number = w
                        break
                    elif w in word_to_num:
                        number = word_to_num[w]
                        break
        else:
            # print partial recognition too
            partial = json.loads(rec.PartialResult())
            if "partial" in partial and partial["partial"]:
                print("DEBUG Partial:", partial["partial"])

# --- Step 4: Save or fail gracefully ---
if number:
    with open("siblings.txt", "w") as f:
        f.write(number + "\n")
    speak(f"Thank you. I saved the number {number} in siblings dot text.")
    print(f"Saved {number} to siblings.txt")
else:
    speak("Sorry, I did not understand a number.")
    print("No number recognized.")
