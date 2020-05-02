#!/usr/bin/env python
# -*- coding: utf-8 -*-
from asyncio import wait
import random
from time import sleep
import cua as c
import threading
import audio as al
import socket
import time
import queue

from poseConnection import posseConnection, connected

HOST = '25.120.131.106'  # Standard loopback interface address (localhost)
PORT = 8005        # Port to listen on (non-privileged ports are > 1023)
classLabels = ['Complain', 'FireAlarm', 'BoilingWater', 'GlassBreak', 'Doorbell', 'Fall', 'CutleryFall', 'HeavyBreath', 'Rain', 'Help', 'RunningWater']
speak = al.speech()

def thread_function_SERVERCONprova(llista):
    print("no es pot conectar server----modo debug on")
    while True:
        e = c.event("garden", int(random.randrange(7)), "2020-04-23 20:11:20.728069", float(0.98))
        llista.appendEvent(e)
        sleep(1)

def thread_function_SERVERCON(llista):
    print("entro connexio servidor")

    try:

        obj = socket.socket()
        obj.connect((HOST, PORT))
        print('Connected by')

    except:
        print("no es pot conectar server----modo debug on")
        while True:
            e = c.event("garden", int("1"), "2020-04-23 20:11:20.728069", float(0.98))
            llista.appendEvent(e)
            sleep(1)

    while True:
        data = str(obj.recv(1024))
        data = data[2:-1]
        print(data)
        info = data.split("%")
        llista = c.ListaEvents()
        e = c.event(info[0], int(info[1]), info[2], float(info[3]))
        llista.appendEvent(e)
        print("location : "+ e.lloc)
        print("type : " + str(e.event))
        print("time : " + e.timeestamp)
        print("confidence : " + str(e.confidence))
        print("-"*50)




# To read from the keyboard without blocking the program              
def read_kbd_input(inputQueue):
    while (True):
        input_str = input()
        inputQueue.put(input_str)
        
def explainSituationVideo():
    print('\n')
    print("#####################################################################")
    print('\n')
    print("In this case the situation is:")
    print('\n')
    print("The user is standing up")
    print('\n')
    print("#####################################################################")
    print('\n')
    
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
    return 0

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
    time.sleep(15)

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
    text = "I am moving arround the house to find you because I detected that the ", evento.event, " ocurred"
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
    
def getWaitTime(timeStart):
    # Get the time waiting for answer
    timeEnd = time.time()
    elapsedTime = timeEnd - timeStart
    hours = elapsedTime // 3600
    elapsedTime = elapsedTime - 3600 * hours
    minutes = elapsedTime // 60
    seconds = elapsedTime - (60 * minutes)
    return minutes, seconds

def main():
    llista = c.ListaEvents()
    try:
        x = threading.Thread(target=thread_function_SERVERCONprova, args=(llista,))
        x.start()
    except:
        print("server not connection")
    speak.reproduceText("hello")
    
    # For reading from the keyboard
    EXIT_COMMAND = "exit"
    inputQueue = queue.Queue()
    
    # Read from the keyboard
    inputThread = threading.Thread(target=read_kbd_input, args=(inputQueue,), daemon=True)
    inputThread.start()
    
    while(True):
        
        # Every 15 minutes the robot will ask again for help if nobody arrives
        quarterHour = 15
        timeRepeatQuestion1 = 30
        timeRepeatQuestion2 = [1, 15]
        timeRepeatQuestion3 = [2, 0]
        
        if llista.anyList() != 0:
            print("-" * 1000)
            explainSituationVideo()
            event = llista.popEvent()
            #robot parla i explica l'event rebut
            print(event.event)
            iniciEvent(event)
            #TODO:robot es mou (navegation)
            print("moure robot ", event.lloc)
            print("el robot arriba al lloc ", "+" * 100)
            #connexio amb el arroyo
            pose = posseConnection()
            pose.startPoseConnnection()
            #TODO: mira si hi ha algu a la habitacio (arroyo)

            while pose.getconection() < 2:
                sleep(0.5)
                print("connection: ", pose.getconection())

            print("pose.persona: ", pose.getpersona())
            if pose.getpersona() == "yes":
                print("hi ha persona", "+" * 50)
                explicacioDeEvent(event)
                while pose.getconection() != 3:
                    sleep(0.5)
                    print("connection: ", pose.getconection())
                print("pose.position: ", pose.getposition())
                
                if pose.getposition() == "dret":
                    print('\n')
                    print("Did you fall and get back up by yourself? [y/n]")
                    
                    # Check input from the keyboard
                    while inputQueue.qsize() <= 0:
                        pass
                    
                    answer = 0
                    while answer == 0:
                        
                        if inputQueue.qsize() > 0:
                            input_str = inputQueue.get()
                    
                            if input_str == EXIT_COMMAND:
                                print("Exiting serial terminal.")
                                break
                            
                            # The answer is yes they fell and got up            
                            if input_str == 'y':
                                
                                # Ask if the user is hurt
                                preguntarEstat()
                                
                                # Check input from the keyboard
                                while inputQueue.qsize() <= 0:
                                    pass
                                
                                while answer == 0:
                                    if inputQueue.qsize() > 0:
                                        input_str = inputQueue.get()
                                
                                        if input_str == EXIT_COMMAND:
                                            print("Exiting serial terminal.")
                                            break
                                        
                                        # The answer is yes --> they are hurt            
                                        if input_str == 'y':
                                            # Flag that indicates if someone arrived to help the user
                                            helpIsHere = 0
                                            # Count how many times the robot asked for help
                                            countTimesHelp = 1
                                            # Flag that indicates if the entered time is an int
                                            timeCheck = 0
                                            
                                             # Ask for help
                                            demanarAjuda()
                                            ferCompanyia()
                                            
                                            askNameHelp()
                                            
                                            # Check input from the keyboard
                                            while inputQueue.qsize() <= 0:
                                                pass
                                            
                                            if inputQueue.qsize() > 0:
                                                input_str = inputQueue.get()
                                                nameHelp = input_str
                                        
                                                if input_str == EXIT_COMMAND:
                                                    print("Exiting serial terminal.")
                                                    break
                                               
                                                askTimeToHelp(nameHelp)
                                                
                                                # Check input from the keyboard
                                                while inputQueue.qsize() <= 0:
                                                    pass
                                                
                                                while timeCheck == 0:
                                                    if inputQueue.qsize() > 0:
                                                        input_str = inputQueue.get()
                                                
                                                        if input_str == EXIT_COMMAND:
                                                            print("Exiting serial terminal.")
                                                            break
                                                        
                                                        try:
                                                            int(input_str)
                                                            timeCheck = 1
                                                            timeUntillHelp = int(input_str)
                                                            print('\n')
                                                            print("OK")
                                                            
                                                        except:
                                                            print('\n')
                                                            print(input_str + " is an invalid answer")
                                                            askTimeToHelp(nameHelp)
                                                            
                                            # Start time to know how much time passed since the robot asked for help            
                                            timeStart = time.time()
                                            # Wait untill the help arrives
                                            while helpIsHere == 0 and timeCheck == 1:
                                                # Get minutes and seconds since timeStart
                                                minutes, seconds = getWaitTime(timeStart)
                                                
                                                # Every 15 minutes ask for help
                                                if minutes == (quarterHour * countTimesHelp):
                                                    demanarAjuda()
                                                    countTimesHelp += 1
                                                
                                                # The person arrived to help the user
                                                if minutes == timeUntillHelp:
                                                    helpIsHere = 1
                                                    helpArrived(nameHelp, event)
                                                    time.sleep(15)
                                                    # END OF TASK #
                                                    
                                        # The answer is no --> they are not hurt 
                                        elif input_str == 'n':
                                            finalProces(event)
                                            retornInici()
                                            time.sleep(15)
                                            # END TASK #
                                        
                                        else:
                                            answer = 0
                                            print('\n')
                                            print(input_str + " is an invalid answer")
                                            preguntarEstat()
                            
                            # The answer is no, the user did not fall at all
                            elif input_str == 'n':
                                answer = 1
                                falseAlarm()
                                finalProces(event)
                                retornInici()
                                time.sleep(15)
                                # END OF TASK #
                            
                            else:
                                answer = 0
                                print('\n')
                                print(input_str + " is an invalid answer")
                                print('\n')
                                print("Did you fall and get back up by yourself? [y/n]")
                    # TODO: acabar interaccio si la persona esta dreta (fer opcions per terminal o random)
                    pose.delete()
                elif pose.getposition() == "sentat":
                    preguntarEstat()
                    # TODO: acabar interaccio si la persona esta sentada (fer opcions per terminal o random)
                    pose.delete()
                elif pose.getposition() == "estirat":
                    
                    # Get the time when the robot asks if the person is hurt
                    timeStart = time.time()
                    
                    # Count how many times the robot asks if the person is hurt
                    i = 0
                    # Flag that indicates if the user has given an answer
                    answer = 0
                    # Flag that indicates if the user is heart (1 = yes, 0 = no)
                    userHurt = 0
    
                    # Ask up to three times preguntarEstat() if there is no reply durint three minutes.
                    preguntarEstat()
                    while i < 3:
                        
                        # Check input from the keyboard
                        if inputQueue.qsize() > 0:
                            input_str = inputQueue.get()
                            answer = 1
                    
                            if input_str == EXIT_COMMAND:
                                print("Exiting serial terminal.")
                                break
                            
                            # The answer is yes --> they are hurt            
                            if input_str == 'y':
                                userHurt = 1
                                i = 4
                            
                            # The answer is no --> they are not hurt 
                            elif input_str == 'n':
                                userHurt = 0
                                i = 4
                            
                            else:
                                print('\n')
                                print(input_str + " is an invalid answer")
                                preguntarEstat()
                                i = 0
                                timeStart = time.time()
                                answer = 0
                            
                        # Count time with no answer from the user
                        if answer == 0:
                            
                            # Get minutes and seconds since timeStart
                            minutes, seconds = getWaitTime(timeStart)
                            
                            if minutes == timeRepeatQuestion3[0] and seconds >= timeRepeatQuestion3[1] :
                                print('\n')
                                print("Three minutes passed with no answer.")
                                i += 1
                            elif i == 1 and minutes == timeRepeatQuestion2[0] and seconds >= timeRepeatQuestion2[1]:
                                i += 1
                                preguntarEstat()
                            elif i == 0 and seconds > timeRepeatQuestion1:
                                i += 1
                                preguntarEstat()
                
                    # Flag that indicates if someone arrived to help the user
                    helpIsHere = 0
                    # Count how many times the robot asked for help
                    countTimesHelp = 1
                    # Flag that indicates if the entered time is an int
                    timeCheck = 0
                    
                    
                    # The user did not reply and the robot has to ask for help
                    if answer == 0:
                        demanarAjuda()
                        ferCompanyia()
                        
                        askNameHelp()
                        
                        # Check input from the keyboard
                        while inputQueue.qsize() <= 0:
                            pass
                        
                        if inputQueue.qsize() > 0:
                            input_str = inputQueue.get()
                            nameHelp = input_str
                    
                            if input_str == EXIT_COMMAND:
                                print("Exiting serial terminal.")
                                break
                            
                            askTimeToHelp(nameHelp)
                                
                            # Check input from the keyboard
                            while inputQueue.qsize() <= 0:
                                pass
                            
                            while timeCheck == 0:
                                if inputQueue.qsize() > 0:
                                    input_str = inputQueue.get()
                            
                                    if input_str == EXIT_COMMAND:
                                        print("Exiting serial terminal.")
                                        break
                                    
                                    try:
                                        int(input_str)
                                        timeCheck = 1
                                        timeUntillHelp = int(input_str)
                                        print('\n')
                                        print("OK")
                                        
                                    except:
                                        print('\n')
                                        print(input_str + " is an invalid answer")
                                        askTimeToHelp(nameHelp)
                                            
                            # Start time to know how much time passed since the robot asked for help            
                            timeStart = time.time()
                            
                            # Wait untill the help arrives
                            while helpIsHere == 0 and timeCheck == 1:
                                # Get minutes and seconds since timeStart
                                minutes, seconds = getWaitTime(timeStart)
                                
                                # Every 15 minutes ask for help
                                if minutes == (quarterHour * countTimesHelp):
                                    demanarAjuda()
                                    countTimesHelp += 1
                                
                                # The person arrived to help the user
                                if minutes == timeUntillHelp:
                                    helpIsHere = 1
                                    helpArrived(nameHelp, event)
                                    time.sleep(15)
                                    # END OF TASK #
                            
                            
                    # Flag that indicates if the user can stand up on their own
                    canStandUp = 0
                    
                    # The user is not hurt
                    if answer == 1 and userHurt == 0:
                        
                        answer = 0
                        # The robot asks the user if they can stand up
                        askStandUp()
                        
                        # Check input from the keyboard
                        while inputQueue.qsize() <= 0:
                            pass
                        
                        while answer == 0:
                            if (inputQueue.qsize() > 0):
                                input_str = inputQueue.get()
                                answer = 1
                        
                                if (input_str == EXIT_COMMAND):
                                    print("Exiting serial terminal.")
                                    break
                                
                                # The answer is yes --> they can stand up            
                                if input_str == 'y':
                                    canStandUp = 1
                                    time.sleep(1)
                                    print('\n')
                                    print("OK")
                                
                                # The answer is no --> they cannot stand up
                                elif input_str == 'n':
                                    canStandUp = 0
                                
                                else:
                                    print('\n')
                                    print(input_str + " is an invalid answer")
                                    askStandUp()
                                    answer = 0
                        
                        # The user can stand up
                        if canStandUp == 1:
                            #TODO: pose detection arroyo
                            # Wait untill the user gets up
                            esperarPersonaPeu()
                            time.sleep(2)
                            print('\n')
                            print("--------------------------------------------------------")
                            print(" ")
                            print("User gets up")
                            print(" ")
                            print("--------------------------------------------------------")
                            
                            # Ask again if the user is hurt to make sure everything is OK
                            preguntarEstat()
                            
                            # Check input from the keyboard
                            while inputQueue.qsize() <= 0:
                                pass
                            
                            answer = 0
                            while answer == 0:
                                if inputQueue.qsize() > 0:
                                    input_str = inputQueue.get()
                            
                                    if (input_str == EXIT_COMMAND):
                                        print("Exiting serial terminal.")
                                        break
                                    
                                    # The answer is yes --> they are hurt            
                                    if input_str == 'y':
                                        answer = 1
                                        userHurt = 1
                                    
                                    # The answer is no --> they are not hurt 
                                    elif input_str == 'n':
                                        finalProces(event)
                                        retornInici()
                                        time.sleep(15)
                                        # END TASK #
                                    
                                    else:
                                        answer = 0
                                        print('\n')
                                        print(input_str + " is an invalid answer")
                                        preguntarEstat()
                        
                        # The user can't stand up
                        else: 
                            
                            # The robots asks if it should get close to help the user stand up
                            preguntaVolAjuda()
                            
                            # Check input from the keyboard
                            while inputQueue.qsize() <= 0:
                                pass
                            
                            answer = 0
                            while answer == 0:
                                if inputQueue.qsize() > 0:
                                    input_str = inputQueue.get()
                            
                                    if input_str == EXIT_COMMAND:
                                        print("Exiting serial terminal.")
                                        break
                                    
                                    # Wants the robot to get closer            
                                    if input_str == 'y':
                                        time.sleep(2)
                                        print('\n')
                                        print("--------------------------------------------------------")
                                        print(" ")
                                        print("The robot gets closer + user stands up")
                                        print(" ")
                                        print("--------------------------------------------------------")
                                        
                                        # Ask again if the user is hurt to make sure everything is OK
                                        preguntarEstat()
                                        
                                        # Check input from the keyboard
                                        while inputQueue.qsize() <= 0:
                                            pass
                                        
                                        while answer == 0:
                                            if inputQueue.qsize() > 0:
                                                input_str = inputQueue.get()
                                        
                                                if input_str == EXIT_COMMAND:
                                                    print("Exiting serial terminal.")
                                                    break
                                                
                                                # The answer is yes --> they are hurt            
                                                if input_str == 'y':
                                                    answer = 1
                                                    userHurt = 1
                                                
                                                # The answer is no --> they are not hurt 
                                                elif input_str == 'n':
                                                    finalProces(event)
                                                    retornInici()
                                                    time.sleep(15)
                                                    # END TASK #
                                                
                                                else:
                                                    answer = 0
                                                    print('\n')
                                                    print(input_str + " is an invalid answer")
                                                    preguntarEstat()
                                    
                                    
                                    # Doesn't want the robot to get closer 
                                    elif input_str == 'n':
                                        
                                        # Flag that indicates if someone arrived to help the user
                                        helpIsHere = 0
                                        # Count how many times the robot asked for help
                                        countTimesHelp = 1
                                        # Flag that indicates if the entered time is an int
                                        timeCheck = 0
                                        
                                        # Ask for help
                                        demanarAjuda()
                                        ferCompanyia()
                                        
                                        askNameHelp()
                                        
                                        # Check input from the keyboard
                                        while inputQueue.qsize() <= 0:
                                            pass

                                        if inputQueue.qsize() > 0:
                                            input_str = inputQueue.get()
                                            nameHelp = input_str
                                    
                                            if input_str == EXIT_COMMAND:
                                                print("Exiting serial terminal.")
                                                break
                                           
                                            askTimeToHelp(nameHelp)
                                            
                                            # Check input from the keyboard
                                            while inputQueue.qsize() <= 0:
                                                pass
                                            
                                            while timeCheck == 0:
                                                if inputQueue.qsize() > 0:
                                                    input_str = inputQueue.get()
                                            
                                                    if input_str == EXIT_COMMAND:
                                                        print("Exiting serial terminal.")
                                                        break
                                                    
                                                    try:
                                                        int(input_str)
                                                        timeCheck = 1
                                                        timeUntillHelp = int(input_str)
                                                        print('\n')
                                                        print("OK")
                                                        
                                                    except:
                                                        print('\n')
                                                        print(input_str + " is an invalid answer")
                                                        askTimeToHelp(nameHelp)
                                                        
                                        # Start time to know how much time passed since the robot asked for help            
                                        timeStart = time.time()
                                        # Wait untill the help arrives
                                        while helpIsHere == 0 and timeCheck == 1:
                                            # Get minutes and seconds since timeStart
                                            minutes, seconds = getWaitTime(timeStart)
                                            
                                            # Every 15 minutes ask for help
                                            if minutes == (quarterHour * countTimesHelp):
                                                demanarAjuda()
                                                countTimesHelp += 1
                                            
                                            # The person arrived to help the user
                                            if minutes == timeUntillHelp:
                                                helpIsHere = 1
                                                helpArrived(nameHelp, event)
                                                time.sleep(15)
                                                # END OF TASK #
                                    
                                    # Invalid answer to getting closer
                                    else:
                                        answer = 0
                                        print('\n')
                                        print(input_str + " is an invalid answer")
                                        preguntaVolAjuda()
                                    
                                    
                    # The user is hurt 
                    
                    # Flag that indicates if someone arrived to help the user
                    helpIsHere = 0
                    # Count how many times the robot asked for help
                    countTimesHelp = 1
                    # Flag that indicates if the entered time is an int
                    timeCheck = 0
                    
                    if answer == 1 and userHurt == 1:
                         # Ask for help
                        demanarAjuda()
                        ferCompanyia()
                        
                        askNameHelp()
                        
                        # Check input from the keyboard
                        while inputQueue.qsize() <= 0:
                            pass
                        
                        if inputQueue.qsize() > 0:
                            input_str = inputQueue.get()
                            nameHelp = input_str
                    
                            if input_str == EXIT_COMMAND:
                                print("Exiting serial terminal.")
                                break
                           
                            askTimeToHelp(nameHelp)
                            
                            # Check input from the keyboard
                            while inputQueue.qsize() <= 0:
                                pass
                            
                            while timeCheck == 0:
                                if inputQueue.qsize() > 0:
                                    input_str = inputQueue.get()
                            
                                    if input_str == EXIT_COMMAND:
                                        print("Exiting serial terminal.")
                                        break
                                    
                                    try:
                                        int(input_str)
                                        timeCheck = 1
                                        timeUntillHelp = int(input_str)
                                        print('\n')
                                        print("OK")
                                        
                                    except:
                                        print('\n')
                                        print(input_str + " is an invalid answer")
                                        askTimeToHelp(nameHelp)
                                        
                        # Start time to know how much time passed since the robot asked for help            
                        timeStart = time.time()
                        # Wait untill the help arrives
                        while helpIsHere == 0 and timeCheck == 1:
                            # Get minutes and seconds since timeStart
                            minutes, seconds = getWaitTime(timeStart)
                            
                            # Every 15 minutes ask for help
                            if minutes == (quarterHour * countTimesHelp):
                                demanarAjuda()
                                countTimesHelp += 1
                            
                            # The person arrived to help the user
                            if minutes == timeUntillHelp:
                                helpIsHere = 1
                                helpArrived(nameHelp, event)
                                time.sleep(15)
                                # END OF TASK #
                    #TODO: acabar interaccio si la persona esta estirada (fer opcions per terminal o random)
                    pose.delete()
            
            # There is nobody in the room
            else:
                print('\n')
                print("There is nobody in the room.")
                
                # The robot looks for the user
                buscarYayo(event)
                
                time.sleep(2)
                print('\n')
                print("--------------------------------------------------------")
                print(" ")
                print("Robot finds the user")
                print(" ")
                print("--------------------------------------------------------")
                
                # The robot explains why it is moving arround
                explicacioDeEventEmptyRoom(event)
                
                # The robot asks if the user is OK to make sure
                preguntarEstat()
                
                timeStart = time.time()
                i = 0
                answer = 0
                while i < 3:
                    
                    # Check input from the keyboard
                    if inputQueue.qsize() > 0:
                        input_str = inputQueue.get()
                        answer = 1
                
                        if input_str == EXIT_COMMAND:
                            print("Exiting serial terminal.")
                            break
                        
                        # The answer is yes --> they are hurt            
                        if input_str == 'y':
                            userHurt = 1
                            i = 4
                        
                        # The answer is no --> they are not hurt 
                        elif input_str == 'n':
                            userHurt = 0
                            i = 4
                        
                        else:
                            print('\n')
                            print(input_str + " is an invalid answer")
                            answer = 0
                            i = 0
                            timeStart = time.time()
                            preguntarEstat()
                        
                    # Count time with no answer from the user
                    if answer == 0:
                        # Get minutes and seconds since timeStart
                        minutes, seconds = getWaitTime(timeStart)
                        
                        if minutes == timeRepeatQuestion3[0] and seconds >= timeRepeatQuestion3[1] :
                            print('\n')
                            print("Three minutes passed with no answer.")
                            i += 1
                        elif i == 1 and minutes == timeRepeatQuestion2[0] and seconds >= timeRepeatQuestion2[1]:
                            i += 1
                            preguntarEstat()
                        elif i == 0 and seconds > timeRepeatQuestion1:
                            i += 1
                            preguntarEstat()
            
            
                # Flag that indicates if someone arrived to help the user
                helpIsHere = 0
                # Count how many times the robot asked for help
                countTimesHelp = 1
                # Flag that indicates if the entered time is an int
                timeCheck = 0
                
                # The user did not reply and the robot has to ask for help
                # Or the answer is that they are hurt
                if answer == 0 or (answer == 1 and userHurt == 1):
                    demanarAjuda()
                    ferCompanyia()
                    
                    askNameHelp()
                    # Check input from the keyboard
                    while inputQueue.qsize() <= 0:
                        pass
                    
                    if inputQueue.qsize() > 0:
                        input_str = inputQueue.get()
                        nameHelp = input_str
                
                        if input_str == EXIT_COMMAND:
                            print("Exiting serial terminal.")
                            break
                       
                        askTimeToHelp(nameHelp)
                        
                        # Check input from the keyboard
                        while inputQueue.qsize() <= 0:
                            pass
                        
                        while timeCheck == 0:
                            if inputQueue.qsize() > 0:
                                input_str = inputQueue.get()
                        
                                if input_str == EXIT_COMMAND:
                                    print("Exiting serial terminal.")
                                    break
                                
                                try:
                                    int(input_str)
                                    timeCheck = 1
                                    timeUntillHelp = int(input_str)
                                    print('\n')
                                    print("OK")
                                    
                                except:
                                    print('\n')
                                    print(input_str + " is an invalid answer")
                                    askTimeToHelp(nameHelp)
                                    
                    # Start time to know how much time passed since the robot asked for help            
                    timeStart = time.time()
                    # Wait untill the help arrives
                    while helpIsHere == 0 and timeCheck == 1:
                        # Get minutes and seconds since timeStart
                        minutes, seconds = getWaitTime(timeStart)
                        
                        # Every 15 minutes ask for help
                        if minutes == (quarterHour * countTimesHelp):
                            demanarAjuda()
                            countTimesHelp += 1
                        
                        # The person arrived to help the user
                        if minutes == timeUntillHelp:
                            helpIsHere = 1
                            helpArrived(nameHelp, event)
                            time.sleep(15)
                            # END OF TASK #
                            
                if answer == 1 and userHurt == 0:
                    falseAlarm()
                    finalProces(event)
                    retornInici()
                    time.sleep(15)
                    # END OF TASK #




if __name__ == "__main__":
    main()