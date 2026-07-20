import speech_recognition as sr
import webbrowser                         
import musiclibrary
import requests
import time
import subprocess
import google.generativeai as genai

newsapi = "5a68338f24e943d5af6209a161ddd1d6"

genai.configure(api_key="AQ.Ab8RN6LeWdwjljAqBR-9sh9fyoCur4ojduCl1Kke_I0QXKOprg") 

model = genai.GenerativeModel(
    model_name="gemini-3.5-flash", 
    system_instruction="You are a virtual assistant named robin skilled in general tasks like Alexa and Google Cloud."
)

chat_session = model.start_chat(history=[])

def speak(text):
    try:
        escaped_text = text.replace("'", "`'")
        cmd = f"Add-Type -AssemblyName System.Speech; (New-Object System.Speech.Synthesis.SpeechSynthesizer).Speak('{escaped_text}')"
        subprocess.run(["powershell", "-Command", cmd], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception as e:
        print(f"Speech Engine Error: {e}")

def aiProcess(command):
    global chat_session 
    
    response = chat_session.send_message(command)
    
    return response.text

def processCommand(c):
    command = c.lower()
    
    if "open google" in command:
        speak("Opening Google")
        webbrowser.open("https://google.com")
        
    elif "open facebook" in command:
        speak("Opening Facebook")
        webbrowser.open("https://facebook.com")
        
    elif "open youtube" in command:
        speak("Opening Youtube")
        webbrowser.open("https://youtube.com")
        
    elif "open linkedin" in command:
        speak("Opening LinkedIn")
        webbrowser.open("https://linkedin.com")
        
    elif command.startswith("play"):
        try:
            song = command.split(" ")[1]                               
            if song in musiclibrary.music:                            # Music Playlist                                   
                link = musiclibrary.music[song]                       # 1.cold  6. HanumanChalisa   
                speak(f"Playing {song}")                              # 2.pink  7. Starboy 
                webbrowser.open(link)                                 # 3.Timeless 8. Bairan
            else:                                                     # 4.Sunflower 9.Sprinter
                speak("Song not found in your music library.")        # 5. bandfourband 10.Hunnids
        except IndexError:
            speak("Which song would you like to play?")

    elif "news" in command:
        speak("Fetching the latest headlines for you.")
        try:
            r = requests.get(f"https://newsapi.org/v2/top-headlines?country=us&apiKey={newsapi}")
            if r.status_code == 200:
                data = r.json()
                articles = data.get('articles', [])
                for article in articles[:5]:
                    speak(article['title'])
                    time.sleep(0.2)
            else:
                speak("I encountered an error fetching the news.")
        except Exception as e:
            speak("I am unable to connect to the internet right now.")
            print(f"News Error: {e}")
            
    # FIXED: Shifted this 'else' block to the left so it aligns with 'if' and 'elif'
    else:
        output = aiProcess(c)
        speak(output)
            

if __name__ == "__main__":
    print("=== Initializing Robin ===")
    speak("Initializing Robin...")
    
    while True:
        r = sr.Recognizer()
        r.dynamic_energy_threshold = True  
        
        try:
            with sr.Microphone() as source:
                print("\n[Loading]: Listening....")
                r.adjust_for_ambient_noise(source, duration=0.5) 
                audio = r.listen(source, timeout=5, phrase_time_limit=3)
            
            print("[Loading]: Processing audio...")
            word = r.recognize_google(audio).lower()
            print(f"-> You said: '{word}'")
            
            if "robin" in word:
                print("-> Success!. Triggering audio response...")
                time.sleep(0.1) 
                speak("How can i help you ?")
                time.sleep(0.1)
                
                with sr.Microphone() as source:
                    print("[Loading]: Robin Activated. Awaiting for your command...")
                    r.adjust_for_ambient_noise(source, duration=0.5)
                    audio = r.listen(source, timeout=5)
                
                command = r.recognize_google(audio)
                print(f"-> Command Heard: '{command}'")
                processCommand(command)
                
        except sr.UnknownValueError:
            pass
        except sr.WaitTimeoutError:
            pass
        except Exception as e:
            print(f"-> System Error: {e}")






