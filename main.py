import pyttsx3
import datetime
import speech_recognition as sr
import smtplib
from access import my_email, my_pass, send_to
from email.message import EmailMessage
import pyautogui
import webbrowser as wb
from time import sleep
import wikipedia
import pywhatkit
from newsapi.newsapi_client import NewsApiClient
import clipboard
import json
import requests
import os
import time as tm
import string
import random
import psutil 
from nltk.tokenize import word_tokenize

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[3].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def showtime():
    time = datetime.datetime.now().strftime("%I:%M:%S")
    speak("The current time is:")
    speak(time)
    
def showdate():
    year = int(datetime.datetime.now().year)
    month = int(datetime.datetime.now().month)
    day = int(datetime.datetime.now().day)
    speak("The current date is:")
    speak(day)
    speak(month)
    speak(year)

def opening():
    hour = datetime.datetime.now().hour
    if hour >= 6 and hour <12:
        speak("Good Morning!")
    elif hour >= 12 and hour <18:
        speak("Good Afternoon!")
    elif hour >= 18 and hour <24:
        speak("Good Evening!")
    else:
        speak("Good Night!")
  
def welcome():
    speak("Welcome back sir!")
    opening()
    speak("Jerry's here, how are can i help you?")

def takecommandcmd():
    query = input("how are can i help you?\n")
    return query

def takecommandmic():
    r = sr.Recognizer() #Reconhecer voz e comandos
    with sr.Microphone() as source:
        print("Listining...")
        r.pause_threshold = 1 #Capturar audio a cada 1 segundo
        audio = r.listen(source)
    try:
        print("Recognizing that...")
        query = r.recognize_google(audio, language='en-US')
        print(query)
    except Exception as e:
        print(e)
        return "None"  
    return query

def sendEmail(receiver, subject, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(my_email, my_pass)
    email = EmailMessage()
    email['From'] = my_email
    email['To'] = receiver
    email['Subject'] = subject
    email.set_content(content)
    server.send_message(email)
    server.close()

def sendwhatsmsg(phone, message):
    Message = message
    wb.open('https://web.whatsapp.com/send?phone='+phone+'&text='+Message)
    sleep(5)
    pyautogui.press('enter')
    
def searchgoogle():
    speak("What should i search?")
    src = takecommandmic()
    wb.open('https://www.google.com/search?q='+src) 
    
def readtext():
    text = clipboard.paste()
    speak(text)
    
def covid_status():
    r = requests.get('https://coronavirus-19-api.herokuapp.com/all')
    data = r.json()
    covid_data = f"Confirmed cases, {data['cases']} \n Deaths, {data['deaths']} \n Recovered, {data['recovered']}"
    speak(covid_data)

def screenshot():
    name_img = tm.time()
    name_img = f'C:\\Users\\Guilherme\\Desktop\\Bot\\screenshot\\{name_img}.png'
    img = pyautogui.screenshot(name_img)
    img.show()
    speak("Screenshot taken sir!")
    
def passwordgen():
    dict_key1 = string.ascii_uppercase
    dict_key2 = string.ascii_lowercase
    dict_key3 = string.digits
    dict_key4 = string.punctuation
    pwd_len = 14
    password = []
    
    password.extend(list(dict_key1))
    password.extend(list(dict_key2))
    password.extend(list(dict_key3))
    password.extend(list(dict_key4))
    
    random.shuffle(password)
    newpassword = ("".join(password[0:pwd_len]))
    print(newpassword)
    speak(newpassword)
    
def usage_cpu():
    usage = str(psutil.cpu_percent())
    speak("CPU status at"+usage)
    battery = psutil.sensors_battery()
    speak("Battery status performance that:")
    speak(battery.percent)
    
if __name__ == "__main__":
    welcome()
    wakename = "jerry"
    while True:
        query = takecommandmic().lower()
        query = word_tokenize(query)
        if wakename in query:
            if "time" in query:
                showtime()
            elif "date" in query:
                showdate()
            elif "email" in query:
                email_list = {
                    'client': 'gpxguii@hotmail.com'
                }
                try:
                    speak("To whom you want to send the mail?")
                    name = takecommandmic()
                    receiver = email_list[name]
                    speak("What's the subject of the mail?")
                    subject = takecommandmic()
                    speak('what should i write to send?')
                    content = takecommandmic()
                    sendEmail(receiver, subject, content)
                    speak('Email has been sent')
                except Exception as e:
                    print(e)
                    speak('Enable to send the email')
                    
            elif "message" in query:
                user_contact = {
                    'girlfriend': ''
                }
                try:
                    speak("To whom you want to send WhatsApp message?")
                    contact = takecommandmic()
                    phone = user_contact[contact]
                    speak("What's the message to send?")
                    message = takecommandmic()
                    sendwhatsmsg(phone, message)
                    speak("Message has been sent!")
                except Exception as e:
                    print(e)
                    speak('Enable to send the message')
            
            elif "wikipedia" in query:
                speak('Searching on Wikipedia...')
                query = query.replace("wikipedia", "")
                result = wikipedia.summary(query, sentences=2)
                print(result)
                speak(result)
            
            elif "search" in query:
                searchgoogle()
                
            elif "youtube" in query:
                speak("Which video should I search for you?")
                src_yt = takecommandmic()
                pywhatkit.playonyt(src_yt)
                
            elif "read" in query:
                readtext()
                
            elif "covid" in query:
                covid_status()
                
            elif "open folder" in query:
                os.system('explorer C://{}'.format(query.replace('Open', '')))
            
            elif "open visual" in query:
                codepath = 'C:\\Users\\Guilherme\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe'
                os.startfile(codepath)
            
            elif "screenshot" in query:
                screenshot()
                
            elif "remember" in query:
                speak("What do you want to remember?")
                data = takecommandmic()
                speak("Reminder"+data)
                remember = open('data.txt','w')
                remember.write(data)
                remember.close()
                
            elif "reminder" in query:
                remember = open('data.txt','r')
                speak("Do you have these reminders..."+remember.read())
                
            elif "create password" in query:
                passwordgen()
                
            elif "usage" in query:
                usage_cpu()
                
            elif "offline" in query:
                speak("Entering in Offline Mode...")
                quit()
        else:
            speak("Can i help you sir?")
        