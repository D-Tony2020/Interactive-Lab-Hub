import speech_recognition as sr
import pygame
import os
import tempfile
import time

class AudioService:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        # Initial calibration
        self.recognizer.energy_threshold = 4000
        self.recognizer.dynamic_energy_threshold = True
        
        try:
            pygame.mixer.init()
        except pygame.error as e:
            print(f"Warning: Audio output not available - {e}")

    def listen(self, timeout=5, phrase_time_limit=10):
        """Record audio from default microphone until silence."""
        try:
            with sr.Microphone() as source:
                print("[Audio] Adjusting for ambient noise...")
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                print("[Audio] Listening...")
                # Listen automatically stops after silence
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
                return audio
        except Exception as e:
            print(f"[Audio] Listen Error: {e}")
            return None

    def play_mp3(self, mp3_content):
        """Play MP3 bytes using Pygame."""
        if not mp3_content:
            return

        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
            f.write(mp3_content)
            temp_path = f.name
        
        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init()
                
            pygame.mixer.music.load(temp_path)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
        except Exception as e:
            print(f"[Audio] Playback Error: {e}")
        finally:
            try:
                pygame.mixer.music.unload()
            except:
                pass
            if os.path.exists(temp_path):
                os.remove(temp_path)

audio_service = AudioService()
