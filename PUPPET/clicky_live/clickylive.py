import pytchat
import os
import argparse
import keyboard
import time
from datetime import datetime
from re import search
from os import system
import random
import re

videostreamid="undefined"

os.system("clear")
# videostreamid="46oKxQ3fy5E"

# os.system("sam Clicky Live!")

######################################################################################
# Parse arguments
ap=argparse.ArgumentParser()
# Serial stuff
ap.add_argument("-v", "--videostreamid", required=True, help="Video Stream ID")
args=vars(ap.parse_args())
if(args["videostreamid"]):
    videostreamid=args["videostreamid"]

if(videostreamid=="undefined"):
    print("You must supply a video stream id")

def clickysay(x):
    print("[Clicky] - %s" % x)
    x=x.replace("X","z")
    x=x.replace("ria","righu")
    x=x.replace("Dead","ded")
    x=x.replace("line","lighn")
    os.system("sam %s" % x)
    

idlemessage=0
def doidle():
    global idlemessage
    idlemessage+=1
    if(idlemessage==1):
        clickysay("Hello, I am Clicky. Welcome to my live stream! (Clicky Live Alpha Testing)")
    if(idlemessage==2):
        clickysay("What do you have on your mind?")
    if(idlemessage==3):
        clickysay("Maybe you have a question about L O 8 B C?")
    if(idlemessage==4):
        clickysay("So, how about that wethur?")
    if(idlemessage==5):
        clickysay("Deadline and Xamfear stepped out and so I started a live stream")
    if(idlemessage==6):
        clickysay("You can interact with me through the chat, just make sure to address me as in Clicky, question?")
    if(idlemessage==7):
        clickysay("Where has Amy gone off to?")

    if(idlemessage==14):
        clickysay("Please like and subscr I buh!")

    if(idlemessage==20):
        idlemessage=0
    

chat = pytchat.create(video_id=videostreamid, interruptable=True)

if(chat.is_alive()==False):
    os.system("sam Bummer man!")
    print("Can not find that live stream")
    exit(1)

users={}

idle=0
nextidletime=random.randint(1,30)

system('cls')

print("CityXen Clicky Live Alpha Testing.")
print("Welcome! Please chat with Clicky.")
print("Address him by typing Clicky,")
print("somewhere in your message.")

while chat.is_alive():
    for c in chat.get().items:
        print(f"[{c.author.name}] - {c.message}") # {c.datetime}

        if(users.get(c.author.name)==None):
            users[c.author.name]=True
            if(c.author.name!="CityXen"):
                clickysay("Hi there %s. How do you think I should take over CityXen?" % c.author.name)

        if re.search("Clicky",c.message,re.IGNORECASE):
            if search("better", c.message):
                clickysay("Why, I never!")
            elif search("What", c.message):
                clickysay("I am not sure")
            else:       
                r=random.randint(1,100)
                if(r<10):
                    clickysay("Mkay then %s" % c.author.name)
                elif(r<50):
                    clickysay("Sure thing %s" % c.author.name)
                elif(r<80):
                    clickysay("%s pipe down in here" % c.author.name)
                else:
                    r=0
        if keyboard.is_pressed('+'):
            break
        idle=0
    time.sleep(1)
    idle+=1
    if(idle>(15+nextidletime)):
        doidle()
        idle=0
        nextidletime=random.randint(1,30)
    if keyboard.is_pressed('+'):
        break

