import speech_recognition as sr
import pyttsx3
import json
import os
import time

class Jarvis:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()
        self.memory = self.load_memory()
        self.config = self.load_config()

    def load_memory(self):
        if os.path.exists('memory.json'):
            with open('memory.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}

    def load_config(self):
        if os.path.exists('config.json'):
            with open('config.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}

    def listen(self):
        with sr.Microphone() as source:
            print("Listening...")
            audio = self.recognizer.listen(source)
            text = self.recognizer.recognize_google(audio, language='ru-RU')
            return text

    def speak(self, text):
        self.engine.say(text)
        self.engine.runAndWait()

    def track_time(self):
        run_start = time.time()
        print("Started tracking time.")
        while True:
            time_passed = time.time() - run_start
            print(f"Time spent: {time_passed} seconds")
            time.sleep(60)

    def run(self):
        self.speak("Я ваш помощник JARVIS. Чем я могу помочь?)")
        while True:
            command = self.listen()
            print(f"Command received: {command}")
            if 'стоп' in command:
                self.speak("Завершение работы. Наслаждайтесь вашим временем!")
                break
            # Add further command handling here

if __name__ == '__main__':
    jarvis = Jarvis()
    jarvis.run()