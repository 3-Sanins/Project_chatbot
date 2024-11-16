import cohere
import speech_recognition as sr
import pyttsx3  # Offline text-to-speech
import requests
from datetime import datetime
import time
import vlc
import yt_dlp

# Replace with your API keys
COHERE_API_KEY = 'N2KVYbjgSfNVKZw2HSwVJCRuRqEVkpFEqCrozr22'
WEATHER_API_KEY = 'b4f806f0e3abdcf366fec65ac964091d'
NEWS_API_KEY = 'bee5cc758c7145cebb9c95cef0c51e2e'

# Initialize the Cohere client
co = cohere.Client(COHERE_API_KEY)

# Initialize pyttsx3 engine
engine = pyttsx3.init()
engine.setProperty("rate", 170)

# Set Indian accent
voices = engine.getProperty('voices')
indian_voice = None
for voice in voices:
    if 'in' in voice.id:  # Check if 'in' is part of the voice ID, commonly used for Indian voices
        indian_voice = voice
        break

if indian_voice:
    engine.setProperty('voice', indian_voice.id)
    print(f"Indian voice set: {indian_voice.name}")
else:
    print("Indian voice not found, using default voice.")

is_speaking = False

def speak(text):
    """Convert text to speech and allow interruption."""
    global is_speaking
    is_speaking = True
    engine.say(text)
    engine.runAndWait()
    is_speaking = False

def stop_speaking():
    """Interrupt the current speech if it's ongoing."""
    if is_speaking:
        engine.stop()  # This will stop pyttsx3 immediately
        print("Speech interrupted.")
    else:
        print("No speech to interrupt.")


def listen():
    """Capture speech input."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        #recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        try:
            print("Processing...")
            text = recognizer.recognize_google(audio)
            print("You:", text)
            return text.lower()
        except sr.UnknownValueError:
            speak("I didn't catch that. Could you repeat?")
        except sr.RequestError:
            speak("Sorry, there's a network error.")
    return None

def play_song(name):
    speak("Please wait for a second")
    """Play a song by searching it on YouTube and streaming its audio."""
    def stream_audio(youtube_url):
        player = vlc.MediaPlayer()

        # Use yt-dlp to extract audio URL
        ydl_opts = {
            'format': 'bestaudio/best',
            'extractaudio': True,  # Extract only audio
            'audioquality': 1,
            'outtmpl': 'audio.%(ext)s',
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(youtube_url, download=False)
            audio_url = info['url']  # Get audio stream URL

        # Play audio using VLC
        media = vlc.Media(audio_url)
        player.set_media(media)
        player.play()

        print("Audio is playing...")
        while True:#player.is_playing():  # Wait until the audio finishes
            time.sleep(1)
            try:
                k=listen().lower()
            except:
                k=''
            if "stop" in k or not player.is_playing():
                player.stop()
                return
        print("Audio stopped.")

    ydl_opts = {
        'quiet': True,  # Disable unnecessary output
        'default_search': 'ytsearch',  # Search YouTube by song name
        'noplaylist': True,  # Only get one result, not a playlist
    }

    # Search YouTube for the song name
    search_query = name
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        result = ydl.extract_info(search_query, download=False)
        if 'entries' in result:
            video = result['entries'][0]  # Get the first video from the search results
            video_url = f"https://www.youtube.com/watch?v={video['id']}"
            stream_audio(video_url)
            return video_url
        else:
            speak("No results found.")
            return None

def get_weather(city):
    """Fetch weather information."""
    city = city.capitalize()
    base_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
    try:
        response = requests.get(base_url)
        response.raise_for_status()  
        data = response.json()
        
        if data.get("main"):
            temperature = data["main"]["temp"]
            weather = data["weather"][0]["description"]
            return f"The temperature in {city} is {temperature}°C with {weather}."
        else:
            return "Couldn't retrieve weather data. Please check the city name or try again later."
    except requests.exceptions.RequestException as e:
        return "I couldn't retrieve the weather data."

def get_news():
    """Fetch the latest news headlines."""
    url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={NEWS_API_KEY}"
    response = requests.get(url).json()
    if response.get("status") != "ok":
        return "I couldn't retrieve the news."
    headlines = [article["title"] for article in response["articles"][:5]]
    return "Here are the latest news headlines: " + "; ".join(headlines)

def get_time():
    """Get the current time."""
    now = datetime.now()
    return now.strftime("The current time is %H:%M.")

def generate_response(user_input):
    """Generate a chatbot response using Cohere API."""
    try:
        response = co.generate(
            model='command', 
            prompt=user_input,
            max_tokens=50,
            temperature=0.7
        )
        data = response.generations[0].text.strip().lower()
        data = data.replace("cohere", "Akshit and friends")
        return data
    except cohere.errors.CohereError as e:
        return "I'm sorry, I encountered an error with my language model."

def chatbot_response(user_input):
    """Handle different types of input like weather, time, and news."""
    if "weather" in user_input:
        city = user_input.split("in")[-1].strip()  
        return get_weather(city)
    elif "time" in user_input:
        return get_time()
    elif "news" in user_input:
        return get_news()
    elif "play" in user_input:
        song_name = user_input.replace("play ", "")
        play_song(song_name)  # Play the song and return None
        return ""
    else:
        return generate_response(user_input)

def handle_user_input():
    """Listen for user input, process it, and respond sequentially."""
    while True:
        user_input = listen()
        if not user_input:
            continue
        if "stop" in user_input:
            if "moving" in user_input:
                pass
            else:
                stop_speaking()

        if "move" in user_input:
            speak("This function can only be used with arduino")

        if user_input in ["bye", "exit", "quit"]:
            speak("Goodbye!")
            
            break

        response = chatbot_response(user_input)
        if response:
            print("Chatbot:", response)
            speak(response)

# Start handling user input in sequence (without threading)
handle_user_input()
