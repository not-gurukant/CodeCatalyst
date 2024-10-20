# Developed by Gurukant
# This code contains a selection of popular songs by Eminem.
print('''---------------------- Developed by Gurukant -----------------------
                               *J.A.R.V.I.S*                                            
                    Just A Rather Very Intelligent System    ''')

#importing all required libraries and modules 
import speech_recognition as sr  #pip install SpeechRecognition
import pyttsx3  #pip install pyttsx3
import webbrowser   #built-in
import pyaudio  #pip install PyAudio
import pyjokes  #pip install pyjokes
#using pyjokes to get a random joke in variable "joke"
joke = pyjokes.get_joke()
#music library 
music = {
    "lose yourself": "https://www.youtube.com/watch?v=_Yhyp-_hX2s",
    "rap god": "https://www.youtube.com/watch?v=XbGs_qK2PQA",
    "not afraid": "https://www.youtube.com/watch?v=j5-yKhDd64s",
    "the real slim shady": "https://www.youtube.com/watch?v=eJO5HU_7_1w",
    "without me": "https://www.youtube.com/watch?v=YVkUvmDQ3HY",
    "mockingbird": "https://www.youtube.com/watch?v=S9bCLPwzSC0",
    "stan": "https://www.youtube.com/watch?v=gOMhN-hfMtY",
    "till i collapse": "https://www.youtube.com/watch?v=ytQ5CYE1VZw",
    "godzilla": "https://www.youtube.com/watch?v=r_0JjYUe5jo",
    "when i'm gone": "https://www.youtube.com/watch?v=1wYNFfgrXTI",
    "the way i am": "https://www.youtube.com/watch?v=MWbP-tE6baA",
    "beautiful": "https://www.youtube.com/watch?v=lgT1AidzRWM",
    "cleanin' out my closet": "https://www.youtube.com/watch?v=RQ9_TKayu9s",
    "love the way you lie": "https://www.youtube.com/watch?v=uelHwf8o7_U",
    "no love": "https://www.youtube.com/watch?v=KV2ssT8lzj8",
    "berzerk": "https://www.youtube.com/watch?v=ab9176Srb5Y",
    "venom": "https://www.youtube.com/watch?v=8CdcCD5V-d8",
    "fall": "https://www.youtube.com/watch?v=MfTbHITdhEI"
}
#An object to recognize audio through mic 
recognizer = sr.Recognizer()
engine = pyttsx3.init()
#Function to make JARVIS speak 
def say(text):
    engine.say(text)
    engine.runAndWait()
print("Just A Rather Very Intelligent System .... JARVIS")
say("Just A Rather Very Intelligent System .... JARVIS ")

print("Initialising JARVIS.....")
say("Initialising JARVIS.....")

print("Welcome to this ultimate desktop assistant developed by Gurukant.")
say("Welcome to this ultimate desktop assistant developed by Gurukant.")

print('Say "JARVIS" to activate ')

#function to process commands 
def process_command(c):
    if (c.lower() == "open google"):
        webbrowser.open("https://www.google.com/")
        say("Opening Google")
    elif(c.lower() == "open youtube"):
        webbrowser.open("https://www.youtube.com/")
        say("Opening YouTube...")
    elif(c.lower() == "open instagram"):
        say("Opening Instagram...")
        webbrowser.open("https://www.instagram.com/")
    elif("joke" in c.lower()):
        say(joke)
        print(joke)
    elif c.lower().startswith("play"):
        song = c.lower().split("play ")[1]
        if song in music:
            link = music[song]
            webbrowser.open(link)
        else:
            print("Song not found.")
            say("Song not found.")

while True:
    # obtain audio from the microphone
    r = sr.Recognizer()

    # recognize speech google
    try:
        with sr.Microphone() as source:
            print("Listening......")
            audio = r.listen(source, timeout=2)
            print("Recognizing.....")
            command = r.recognize_google(audio)
            print(command)
        
        #Listen for the command 
        if command.lower() == "jarvis":
            say("Yes, how can I help you?")
            with sr.Microphone() as source:
                print("Listening....")
                audio = r.listen(source, timeout=3)
                print("Recognizing.........")
                command = r.recognize_google(audio)
                process_command(command)
          
    except Exception as e:
        print("Something went wrong :(; {0}".format(e))
