import os 
import webbrowser
from config import apikey  # Your API key configuration
import datetime
import random
import numpy as np
from google.cloud import aiplatform  # Import Google Cloud AI platform for Gemini AI integration
import speech_recognition as sr
import pyttsx3

chatStr = ""  # To store the ongoing conversation history

# Initialize the AI platform with your Google Cloud credentials
aiplatform.init(project="548707354068", location="us-central1")

# Function to handle chat interactions with the AI
def chat(query):
    global chatStr
    print(chatStr)
    chatStr += f"shafa: {query}\n Jarvis: "

    try:
        response = aiplatform.gapic.PredictionServiceClient().predict(
            endpoint="projects/your_project_id/locations/your_location/endpoints/your_endpoint_id",  # Replace with actual endpoint
            instances=[{"content": query}],
        )
        response_text = response.predictions[0]
        say(response_text)
        chatStr += f"{response_text}\n"
        return response_text
    except Exception as e:
        print(f"Error during AI prediction: {e}")
        return "Sorry, I couldn't process that right now."

# Function for AI response to prompts
def ai(prompt):
    text = f"Gemini AI response for Prompt: {prompt} \n *************************\n\n"
    
    try:
        response = aiplatform.gapic.PredictionServiceClient().predict(
            endpoint="projects/your_project_id/locations/your_location/endpoints/your_endpoint_id",  # Replace with actual endpoint
            instances=[{"content": prompt}],
        )
        response_text = response.predictions[0]
        text += response_text
        
        if not os.path.exists("GeminiAI"):
            os.mkdir("GeminiAI")

        with open(f"GeminiAI/{''.join(prompt.split('intelligence')[1:]).strip() }.txt", "w") as f:
            f.write(text)
    except Exception as e:
        print(f"Error during AI prediction: {e}")
        text += "Sorry, there was an issue with processing your request."

# Function to say output aloud using pyttsx3 with a deeper, slower, and clearer voice
def say(text):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)  # Change to a different voice
    engine.setProperty('rate', 130)  # Slow down speech rate further
    engine.setProperty('volume', 1.0)  # Ensure maximum volume
    engine.say(text)
    engine.runAndWait()

# Function to listen to user's voice commands
def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        try:
            print("Recognizing...")
            say("Recognizing...")
            query = r.recognize_google(audio, language="en-in")
            print(f"User said: {query}")
            say(f"You said: {query}")
            return query
        except Exception as e:
            print(f"Error recognizing speech: {e}")
            say("Sorry, I couldn't understand that. Please say again.")
            return "Some Error Occurred. Sorry from Jarvis"
        

# Main program to handle commands and responses
if __name__ == '__main__':
    print('Welcome to Jarvis A.I')
    say("At your service sir!")
    
    while True:
        print("Listening...")
        say("How can I help you?")
        query = takeCommand()
        
        sites = [["youtube", "https://www.youtube.com"], ["wikipedia", "https://www.wikipedia.com"], ["google", "https://www.google.com"]]
        for site in sites:
            if f"Open {site[0]}".lower() in query.lower():
                say(f"Opening {site[0]} sir...")
                webbrowser.open(site[1])

        if "music" in query:
            musicPath = "E:/mp3/1.mp3"  # Replace with correct music path
            os.startfile(musicPath)

        elif "time" in query:
            local_time = datetime.datetime.now()
            hour = local_time.strftime("%I")
            minute = local_time.strftime("%M")
            am_pm = local_time.strftime("%p")
            say(f"Sir, the current local time is {hour} hours and {minute} minutes {am_pm}")

        elif "date" in query:
            local_date = datetime.datetime.now()
            date = local_date.strftime("%B %d, %Y")
            say(f"Sir, today's date is {date}")

        elif "who i am" in query:
            say("If you talk then definitely you're human.")
            
        elif "open facetime" in query.lower():
            os.startfile("C:/Path/To/Your/FaceTimeApp.exe")

        elif "open pass" in query.lower():
            os.startfile("C:/Path/To/PasskyApp.exe")

        elif "Using artificial intelligence" in query.lower():
            ai(prompt=query)

        elif "Quit" in query.lower():
            exit()

        elif "reset" in query.lower():
            chatStr = ""
            say("Chat history has been reset.")
        else:
            print("Chatting...")
            chat(query)