#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import audio as al
import time

classLabels = ['Complain', 'FireAlarm', 'BoilingWater', 'GlassBreak', 'Doorbell', 'Fall', 'CutleryFall', 'HeavyBreath', 'Rain', 'Help', 'RunningWater']
speak = al.speech()

        
def iniciEvent(evento):
    print('\n')
    print("The " + evento.event + " event has ocurred and I am going to the " + evento.lloc + " to check what happened.")
    text = "The " + evento.event + " event has ocurred and I am going to the " + evento.lloc + " to check what happened."
    speak.reproduceText(text)
    return 0

def explicacioDeEvent(evento):
    time.sleep(1)
    print('\n')
    print("I detected that the ", evento.event, " event ocurred and I came to check if everything is OK.")
    text = "I detected that the "+ evento.event+ " event ocurred and I came to check if everything is OK."
    speak.reproduceText(text)
    return 0

def explicacioDeEventEmptyRoom(evento):
    time.sleep(1)
    print('\n')
    print("I detected that the ", evento.event, " event ocurred and I went to " + evento.lloc + " to check it but I did not find you there.")
    text = "I detected that the "+ evento.event+ " event ocurred and I went to " + evento.lloc + " to check it but I did not find you there."
    speak.reproduceText(text)
    
def explicacioDeEventInfo(evento):
    time.sleep(1)
    print('\n')
    print("I detected that the ", evento.event, " event ocurred and I came to make sure you were aware of this.")
    text = "I detected that the "+ evento.event+ " event ocurred and I came to make sure you were aware of this."
    speak.reproduceText(text)

def askAwareEventInfo():
    time.sleep(1)
    print('\n')
    print("Are you aware of this?")
    text = "Are you aware of this?"
    speak.reproduceText(text)
    
def preguntarEstat():
    print('\n')
    print("Are you hurt? [y/n]")
    text = "Are you hurt?"
    speak.reproduceText(text)
    return 0

def askStandUp():
    time.sleep(1)
    print('\n')
    print("Can you stand up on your own? [y/n]")
    text = "Can you stand up on your own?"
    speak.reproduceText(text)

def demanarAjuda():
    time.sleep(1)
    print('\n')
    print("Contacting someone for help...")
    text = "Contacting someone for help..."
    speak.reproduceText(text)

def preguntaVolAjuda():
    time.sleep(1)
    print('\n')
    print("Do you want me to get closer to help you get up? [y/n]")
    text = "Do you want me to get closer to help you get up?"
    speak.reproduceText(text)

def explicacioSituacioResponsable(evento):
    time.sleep(1)
    print('\n')
    print("I detected that the ", evento.event, " event ocurred at ", evento.timeestamp, " o'clock and I went to ", evento.lloc, " to check the situation and I asked for help." )
    text = "I detected that the "+ evento.event+ " event ocurred at "+ evento.timeestamp+ " o'clock and I went to "+ evento.lloc+ " to check the situation and I asked for help"
    speak.reproduceText(text)

def finalProces(evento):
    time.sleep(1)
    print('\n')
    print("The task related to the ", evento.event, " event is finished and I will return to the resting point.")
    text = "The task related to the "+ evento.event+ " event is finished and I will return to the resting point."
    speak.reproduceText(text)
    return 0

def retornInici():
    time.sleep(2)
    print('\n')
    print("I am going to the resting point.")
    text = "I am going to the resting point"
    speak.reproduceText(text)
    time.sleep(0.5)

def ferCompanyia():
    time.sleep(2)
    print('\n')
    print("I will stay here with you untill someone arrives.")
    text = "I will stay here with you untill someone arrives"
    speak.reproduceText(text)

def analitzaResposta():
    pass

def esperarPersonaPeu():
    time.sleep(2)
    print('\n')
    print("I will wait untill you get up to make sure you are OK.")
    text = "I will wait untill you get up to make sure you are OK"
    speak.reproduceText(text)

def buscarYayo(evento):
    time.sleep(2)
    print('\n')
    print("I am moving arround the house to find you because I detected that the ", evento.event, " ocurred.")
    text = "I am moving arround the house to find you because I detected that the "+ evento.event+ " ocurred"
    speak.reproduceText(text)

def falseAlarm():
    time.sleep(1)
    print('\n')
    print("Sorry, it was a false alarm then.")
    text = "Sorry, it was a false alarm then"
    speak.reproduceText(text)

def askNameHelp():
    time.sleep(1)
    print('\n')
    print(">>>> Type the name of the person who should contact the robot: ")
    
def askTimeToHelp(nameHelp):
    time.sleep(1)
    print('\n')
    print(">>>> How long will it take for " + nameHelp + " to arrive? (in minutes)")

def helpArrived(nameHelp, evento):
    print('\n')
    print(nameHelp + " arrived.")
    text = nameHelp + " arrived"
    speak.reproduceText(text)
    explicacioSituacioResponsable(evento)
    finalProces(evento)
    retornInici()
    
def askEventHappened():
    print('\n')
    print("Did this event happen? [y/n]")
    text = "Did this event happen?"
    speak.reproduceText(text)

def askFall():
    print('\n')
    print("Did you fall and get back up by yourself? [y/n]")
    text = "Did you fall and get back up by yourself?"
    speak.reproduceText(text)
    
def invalidAnswer():
    print("Sorry, I didn't understand your answer.")
    text = "Sorry, I didn't understand your answer."
    speak.reproduceText(text)

def InformRobotCannotMove():
    print("the robot can't go to the place.")
    text = "the robot can't go to the place."
    speak.reproduceText(text)
    
def StartMoving(evento):
    print("I'm starting to move towards " + evento)
    text = ("I'm starting to move towards" + evento)
    speak.reproduceText(text)

def nobodyintheRoom():
    print("-" * 100)
    print('\n')
    print("*")
    print(" There is nobody in the room.")