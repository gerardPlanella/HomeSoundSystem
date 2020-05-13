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
import actions as ac
import comprovations as co
import emptyRoom as er
import standingUp as su
import layDown as ld
import fitxerProves

from poseConnection import posseConnection, connected

HOST = '25.120.131.106'  # Standard loopback interface address (localhost)
PORT = 8001        # Port to listen on (non-privileged ports are > 1023)
classLabels = ['Complain', 'FireAlarm', 'BoilingWater', 'GlassBreak', 'Doorbell', 'Fall', 'CutleryFall', 'HeavyBreath', 'Rain', 'Help', 'RunningWater','Silence']
speak = al.speech()

def thread_function_SERVERCONprova(llista):
    print("no es pot conectar server----modo debug on")
    while True:
        e = c.event("garden", int(random.randrange(10)), "2020-04-23 20:11:20.728069", float(0.98))
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


def read_kbd_input(inputQueue):
    while (True):
        input_str = input()
        inputQueue.put(input_str)


def main():
    llista = c.ListaEvents()
    try:
        #connexion con el servidor
        #x = threading.Thread(target = thread_function_SERVERCON(llista), args=(llista,))
        #prova
        x = threading.Thread(target= fitxerProves.thread_function_prava3funcionsIgualsalMateixTemps(llista), args=(llista,))
        x.start()
    except:
        print("server not connection")

    inputQueue = queue.Queue()

    # # Read from the keyboard
    inputThread = threading.Thread(target=read_kbd_input, args=(inputQueue,), daemon=True)
    inputThread.start()

    while(True):
        if llista.anyList() != 0:

            event = llista.popEvent()
            #robot parla i explica l'event rebut
            print("-"*60, " START", event.event, "-"*60, "\n")
            ac.iniciEvent(event)
            #TODO:robot es mou (navegation)
            print("\nThe robot moves towards ", event.lloc, "\n")
            sleep(0.5)
            print("the robot arrives to the ", event.lloc, "\n")
            #connexio amb el arroyo
            pose = posseConnection()
            pose.startPoseConnnection()
            while pose.getconection() < 2:
                sleep(0.5)

            print("-"*100)
            print("Is there a person? ", pose.getpersona())
            if pose.getpersona() == "yes":

                while pose.getconection() != 3:
                    sleep(0.5)
                pose.delete()
                print("What position is the person in? ", pose.getposition())
                print("-" * 100)
                
                if pose.getposition() == "dret" or pose.getposition() == "sentat" :
                    # Event where the robot only has to inform the user that they occurred
                    if event.event == 'FireAlarm' or event.event == 'Doorbell' or event.event == 'RunningWater' or event.event == 'Rain':
                        su.infoEvent(event, inputQueue)

                    elif event.event == 'Fall':
                        ac.explicacioDeEvent(event)
                        su.eventFall(event, inputQueue)

                    # Other events
                    else:
                        ac.explicacioDeEvent(event)
                        su.otherEvent(event, inputQueue)



                elif pose.getposition() == "estirat":
                    # Ask up to three times preguntarEstat() if there is no reply durint three minutes.
                    ac.preguntarEstat()

                    # Wait for the user to answer
                    answer, userHurt, numInvalidAnswer = co.waitAnswerEstat(inputQueue)

                    if answer == 0 or numInvalidAnswer == 5:
                        ld.askForHelpLD(inputQueue, event)

                    # The user is not hurt
                    if answer == 1 and userHurt == 0:

                        answer = 0
                        # The robot asks the user if they can stand up
                        ac.askStandUp()

                        # Ask if the user can stand up = 3
                        yesNo = co.waitYesNoAnswer(inputQueue, 3)

                        if yesNo == 'y':
                            # Flag that indicates if the user can stand up on their own
                            canStandUp = 1
                            time.sleep(1)
                            print('\n')
                            print("OK")

                        if yesNo == 'n':
                            # Flag that indicates if the user can stand up on their own
                            canStandUp = 0

                        # The user can stand up
                        if canStandUp == 1:
                            # TODO: pose detection arroyo
                            ld.waitStandUp(inputQueue, event)

                        # The user can't stand up
                        else:

                            # The robots asks if it should get close to help the user stand up
                            ac.preguntaVolAjuda()

                            # Pregunta vol ajuda = 4
                            yesNo = co.waitYesNoAnswer(inputQueue, 4)

                            # The user wants the robot to get closer to help
                            if yesNo == 'y':
                                ld.helpStandUp(inputQueue, event)

                            # The user doesn't want the robot to get closer
                            if yesNo == 'n':
                                ld.askForHelpLD(inputQueue, event)

                                # The user is hurt
                    if answer == 1 and userHurt == 1:
                        ld.askForHelpLD(inputQueue, event)

                    # TODO: acabar interaccio si la persona esta estirada (fer opcions per terminal o random)

            # There is nobody in the room
            else:
                pose.delete()
                print("-" * 100)
                print('\n')
                print("*")
                print(" There is nobody in the room.")

                # The robot looks for the user
                ac.buscarYayo(event)

                time.sleep(2)
                print('\n')
                print("-"*100)
                print("Robot finds the user")
                print("-"*100)

                # Event where the robot only has to inform the user that they occurred
                if event.event == 'FireAlarm' or event.event == 'Doorbell' or event.event == 'RunningWater' or event.event == 'Rain':
                    er.infoEvent(event, inputQueue)

                else:
                    er.askIfEventHappened(event, inputQueue)

            llista.eventRemove(event)
            
            print("The robot arrives to the resting point\n")
            print("-"*50, "END TASK", "-"*50)

if __name__ == "__main__":
    main()