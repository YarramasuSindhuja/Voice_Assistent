# Voice Assistant - "Hey Siri" Clone

A Python-based voice assistant that works like "Hey Siri" with wake word detection and various voice commands.

## Features

- **Wake Word Detection**: Say "Hey Siri" to activate the assistant
- **Voice Commands**: Natural language processing for various tasks
- **Text-to-Speech**: The assistant responds with voice feedback
- **Multiple Functions**: Time, date, web search, Wikipedia, YouTube, weather, jokes, and more

## Supported Commands

### Basic Information
- "What time is it?" - Get current time
- "What day is it?" - Get current date
- "Tell me a joke" - Get a random joke

### Web & Search
- "Open Google" - Open Google website
- "Open YouTube" - Open YouTube website
- "Search for [query]" - Search Google
- "Play [video] on YouTube" - Search YouTube
- "What is [topic]" - Search Wikipedia

### Weather (requires API key)
- "What's the weather in [city]?" - Get weather information

### Reminders
- "Remind me to [task]" - Set a reminder

### System
- "Help" - Show available commands
- "Goodbye" or "Exit" - Close the assistant

## Installation

### Prerequisites
- Python 3.7 or higher
- Microphone (built-in or external)
- Speakers or headphones

### Step 1: Install Python Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Install PyAudio (if not working)
If you encounter issues with PyAudio installation:

**Windows:**
```bash
pip install pipwin
pipwin install pyaudio
```

**macOS:**
```bash
brew install portaudio
pip install pyaudio
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install python3-pyaudio portaudio19-dev
pip install pyaudio
```

### Step 3: Optional - Weather API Setup
For weather functionality, get a free API key from [OpenWeatherMap](https://openweathermap.org/api):
1. Sign up for a free account
2. Get your API key
3. Uncomment and add your API key in `main.py`:
```python
assistant.weather_api_key = "your_api_key_here"
```

## Usage

### Running the Assistant
```bash
python main.py
```

### How to Use
1. Run the program
2. Say "Hey Siri" to activate the assistant
3. Wait for "Yes, how can I help you?" response
4. Speak your command clearly
5. The assistant will respond with voice and text

### Example Interactions
```
You: "Hey Siri"
Assistant: "Yes, how can I help you?"
You: "What time is it?"
Assistant: "The current time is 2:30 PM"

You: "Hey Siri"
Assistant: "Yes, how can I help you?"
You: "Tell me a joke"
Assistant: [Tells a random joke]

You: "Hey Siri"
Assistant: "Yes, how can I help you?"
You: "Search for Python programming"
Assistant: "Searching Google for Python programming"
```

## Troubleshooting

### Common Issues

1. **"No module named 'pyaudio'"**
   - Install PyAudio using the instructions above

2. **"Could not understand audio"**
   - Speak clearly and ensure your microphone is working
   - Check microphone permissions in your OS settings

3. **"Could not request results"**
   - Check your internet connection
   - Google Speech Recognition requires internet access

4. **Voice not working**
   - Ensure speakers/headphones are connected and working
   - Check system volume settings

### Performance Tips
- Use a good quality microphone for better recognition
- Speak clearly and at a normal pace
- Reduce background noise
- Ensure stable internet connection

## Customization

### Changing the Wake Word
Edit line 28 in `main.py`:
```python
self.wake_word = "hey Siri"  # Change to your preferred wake word
```

### Adding New Commands
Add new command patterns in the `process_command` method:
```python
elif any(word in command for word in ["your", "command", "words"]):
    return self.your_new_function()
```

### Changing Voice Settings
Modify voice properties in the `__init__` method:
```python
self.engine.setProperty('rate', 150)  # Speed (words per minute)
self.engine.setProperty('volume', 0.9)  # Volume (0.0 to 1.0)
```

## Dependencies

- **SpeechRecognition**: Speech-to-text conversion
- **pyttsx3**: Text-to-speech conversion
- **wikipedia**: Wikipedia search functionality
- **pywhatkit**: Web automation features
- **pyjokes**: Joke generation
- **requests**: HTTP requests for weather API
- **PyAudio**: Audio input/output handling

## License

This project is open source and available under the MIT License.

## Contributing

Feel free to contribute by:
- Adding new voice commands
- Improving speech recognition accuracy
- Adding new features
- Fixing bugs

## Support

If you encounter any issues:
1. Check the troubleshooting section above
2. Ensure all dependencies are properly installed
3. Verify your microphone and speakers are working
4. Check your internet connection for speech recognition features
