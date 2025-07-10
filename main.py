import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import webbrowser
import pywhatkit
import os
import pyjokes
import sys
import time
import json
import requests
from threading import Thread
import queue

class VoiceAssistant:
    def __init__(self):
        # Initialize speech recognition and text-to-speech
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()
        
        # Configure voice settings
        voices = self.engine.getProperty('voices')
        if voices:
            self.engine.setProperty('voice', voices[0].id)  # Index 0 for male voice, 1 for female
        self.engine.setProperty('rate', 150)  # Speed of speech
        
        # Wake word
        self.wake_word = "hey siri"
        self.is_listening = False
        
        # Command queue for threading
        self.command_queue = queue.Queue()
        
        # User preferences
        self.user_name = "User"
        self.weather_api_key = None  # You can add your OpenWeatherMap API key here
        
    def speak(self, text):
        """Convert text to speech"""
        print(f"Assistant: {text}")
        try:
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            print(f"[DEBUG] pyttsx3 error: {e}")
            print("[DEBUG] Could not speak the response. Please check your audio setup.")
        
    def listen(self):
        """Listen for voice input"""
        with sr.Microphone() as source:
            print("Listening...")
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
            try:
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
                return audio
            except sr.WaitTimeoutError:
                return None
                
    def recognize_speech(self, audio):
        """Convert speech to text"""
        try:
            text = self.recognizer.recognize_google(audio)
            print(f"You said: {text}")
            # Ensure text is a string before calling lower()
            if isinstance(text, str):
                return text.lower()
            else:
                print(f"[DEBUG] Unexpected type from recognize_google: {type(text)}")
                return str(text).lower()
        except sr.UnknownValueError:
            print("Could not understand audio")
            return None
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
            return None
            
    def detect_wake_word(self, text):
        """Check if wake word is detected"""
        return self.wake_word in text.lower()
        
    def get_time(self):
        """Get current time"""
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        return f"The current time is {current_time}"
        
    def get_date(self):
        """Get current date"""
        current_date = datetime.datetime.now().strftime("%B %d, %Y")
        return f"Today is {current_date}"
        
    def search_wikipedia(self, query):
        """Search Wikipedia"""
        try:
            # Remove common words from query
            query = query.replace("search", "").replace("wikipedia", "").replace("for", "").strip()
            result = wikipedia.summary(query, sentences=2)
            return f"According to Wikipedia: {result}"
        except:
            return "Sorry, I couldn't find that on Wikipedia."
            
    def open_website(self, url):
        """Open a website"""
        try:
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
            webbrowser.open(url)
            return f"Opening {url}"
        except:
            return "Sorry, I couldn't open that website."
            
    def play_youtube(self, query):
        """Play YouTube video"""
        try:
            # Clean the query and encode it properly
            clean_query = query.strip()
            if not clean_query:
                print("[DEBUG] No search query provided for YouTube.")
                return "Please specify what you want to search on YouTube."
            
            # Use webbrowser to open YouTube search
            search_url = f"https://www.youtube.com/results?search_query={clean_query.replace(' ', '+')}"
            print(f"[DEBUG] Opening YouTube URL: {search_url}")
            result = webbrowser.open_new_tab(search_url)
            print(f"[DEBUG] webbrowser.open_new_tab returned: {result}")
            return f"Searching YouTube for {clean_query}"
        except Exception as e:
            print(f"[DEBUG] Error opening YouTube: {e}")
            return "Sorry, I couldn't search YouTube."
            
    def search_google(self, query):
        """Search Google"""
        try:
            # Use webbrowser to open Google search
            search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
            webbrowser.open(search_url)
            return f"Searching Google for {query}"
        except:
            return "Sorry, I couldn't search Google."
            
    def tell_joke(self):
        """Tell a joke"""
        joke = pyjokes.get_joke()
        return joke
        
    def get_weather(self, city):
        """Get weather information (requires API key)"""
        if not self.weather_api_key:
            return "Weather feature requires an API key. Please add your OpenWeatherMap API key to use this feature."
        
        try:
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={self.weather_api_key}&units=metric"
            response = requests.get(url)
            data = response.json()
            
            if data["cod"] == 200:
                temp = data["main"]["temp"]
                description = data["weather"][0]["description"]
                return f"The weather in {city} is {temp}°C with {description}"
            else:
                return f"Sorry, I couldn't get weather information for {city}"
        except:
            return "Sorry, I couldn't get weather information."
            
    def set_reminder(self, text):
        """Set a reminder (basic implementation)"""
        # This is a basic implementation. You could enhance it with actual reminder functionality
        return f"Reminder set: {text}"
        
    def process_command(self, command):
        """Process voice commands"""
        if not command:
            return
            
        # Time commands
        if any(word in command for word in ["time", "what time"]):
            return self.get_time()
            
        # Date commands
        elif any(word in command for word in ["date", "what day", "today"]):
            return self.get_date()
            
        # Wikipedia search
        elif any(word in command for word in ["wikipedia", "search for", "what is", "who is"]):
            return self.search_wikipedia(command)
            
        # Website commands
        elif any(word in command for word in ["open", "go to", "visit"]):
            if "google" in command:
                return self.open_website("google.com")
            elif "youtube" in command:
                return self.open_website("youtube.com")
            elif "facebook" in command:
                return self.open_website("facebook.com")
            else:
                # Extract website from command
                words = command.split()
                for i, word in enumerate(words):
                    if word in ["open", "go", "visit"] and i + 1 < len(words):
                        return self.open_website(words[i + 1])
                        
        # YouTube commands
        elif any(word in command for word in ["play", "youtube", "video"]):
            # Extract the search query more intelligently
            query = command.lower()
            # Remove common trigger words
            for word in ["play", "on", "youtube", "video", "videos", "search", "for"]:
                query = query.replace(word, "")
            query = query.strip()
            print(f"Extracted YouTube query: '{query}'")  # Debug print
            return self.play_youtube(query)
            
        # Google search
        elif any(word in command for word in ["search", "google"]):
            query = command.replace("search", "").replace("google", "").replace("for", "").strip()
            return self.search_google(query)
            
        # Joke commands
        elif any(word in command for word in ["joke", "funny", "humor"]):
            return self.tell_joke()
            
        # Weather commands
        elif any(word in command for word in ["weather", "temperature"]):
            # Extract city name from command
            words = command.split()
            for i, word in enumerate(words):
                if word in ["weather", "temperature"] and i + 1 < len(words):
                    city = words[i + 1]
                    return self.get_weather(city)
            return self.get_weather("London")  # Default city
            
        # Reminder commands
        elif any(word in command for word in ["remind", "reminder", "set reminder"]):
            reminder_text = command.replace("remind me to", "").replace("set reminder", "").replace("reminder", "").strip()
            return self.set_reminder(reminder_text)
            
        # System commands
        elif any(word in command for word in ["exit", "quit", "stop", "goodbye"]):
            self.speak("Goodbye! Have a great day!")
            sys.exit()
            
        # Help command
        elif any(word in command for word in ["help", "what can you do", "commands"]):
            return """I can help you with:
            - Time and date
            - Wikipedia searches
            - Opening websites
            - Playing YouTube videos
            - Google searches
            - Telling jokes
            - Weather information
            - Setting reminders
            - And more!"""
            
        else:
            return "I'm sorry, I didn't understand that command. Try saying 'help' to see what I can do."
            
    def run(self):
        """Main loop for the voice assistant"""
        self.speak("Hello! I'm your voice assistant. Say 'Hey Siri' to activate me, or 'help' to see what I can do.")

        while True:
            try:
                # Listen for wake word
                audio = self.listen()
                if audio:
                    text = self.recognize_speech(audio)
                    print(f"[DEBUG] Recognized text: {text}")
                    if text and self.detect_wake_word(text):
                        print("[DEBUG] Wake word detected.")
                        self.speak("Yes, how can I help you?")

                        # Listen for command
                        command_audio = self.listen()
                        if command_audio:
                            command = self.recognize_speech(command_audio)
                            print(f"[DEBUG] Command recognized: {command}")
                            if command:
                                response = self.process_command(command)
                                print(f"[DEBUG] Response to speak: {response}")
                                if response:
                                    self.speak(response)
                            else:
                                print("[DEBUG] No command recognized.")
                        else:
                            print("[DEBUG] No command audio detected.")
                    else:
                        print("[DEBUG] Wake word not detected.")
                else:
                    print("[DEBUG] No audio detected.")
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
            except Exception as e:
                print(f"Error: {e}")
                continue

def main():
    """Main function to run the voice assistant"""
    assistant = VoiceAssistant()
    
    # Optional: Set your OpenWeatherMap API key for weather features
    # assistant.weather_api_key = "your_api_key_here"
    
    print("Voice Assistant Starting...")
    print("Say 'Hey Siri' to activate the assistant")
    print("Press Ctrl+C to exit")
    
    assistant.run()

if __name__ == "__main__":
    main()

