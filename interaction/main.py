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
from ConnectionPlusNavegation import NavegationStarts, SearchForPerson, askPose, NavegationEnd, searchForSomeone
from Person import personaDreta, personaEstirada

from poseConnection import posseConnection, connected

HOST = '25.120.131.106'  # Standard loopback interface address (localhost)
PORT = 8001        # Port to listen on (non-privileged ports are > 1023)
classLabels = ['Complain', 'FireAlarm', 'BoilingWater', 'GlassBreak', 'Doorbell', 'Fall', 'CutleryFall', 'HeavyBreath', 'Rain', 'Help', 'RunningWater','Silence']
speak = al.speech()

def thread_function_SERVERCONprova(llista):
    print("no es pot conectar server----modo debug on")
    while True:
        e = c.event("kitchen", int(random.randrange(10)), "2020-04-23 20:11:20.728069", float(0.98))
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
            e = c.event("bathroom", int("1"), "2020-04-23 20:11:20.728069", float(0.98))
            llista.appendEvent(e)
            sleep(1)

    while True:
        print("hola abans rebo objecte")
        data = str(obj.recv(1024))
        print("hola despres rebo objecte")
        data = data[2:-1]
        print(data)
        if (data == " "):
            print ("estic rebent merda")
        else:
            info = data.split("%")
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
        x = threading.Thread(target = thread_function_SERVERCON, args=(llista,))
        #prova
        #x = threading.Thread(target= fitxerProves.thread_function_pravaTotesFuncions(llista), args=(llista,))
        x.start()
    except:
        print("server Miquel not connection")


    inputQueue = queue.Queue()
    # # Read from the keyboard
    inputThread = threading.Thread(target=read_kbd_input, args=(inputQueue,), daemon=True)
    inputThread.start()

    print("abans del while")
    while(True):
        #print(llista)
        if llista.anyList() != 0:
            event = llista.popEvent()
            #robot parla i explica l'event rebut
            print("-"*60, " START", event.event, "-"*60, "\n")
            ac.iniciEvent(event)

            #connecto amb la navegació
            navOK = NavegationStarts(event)

            #la connexion ha sido un exito i he llegado al sitio
            if navOK == "OK":
                print("the robot arrives to the ", event.lloc, "\n")
                pose = posseConnection()
                print("abans de search for a person")
                person = SearchForPerson(pose)
                print("-" * 100)
                print("Is there a person? ", person)

                if person == "yes":
                    position = askPose(pose)
                    print("What position is the person in? ", position)
                    print("-" * 100)

                    if position == "dret" or position == "sentat":
                        personaDreta(event, inputQueue)

                    elif position == "estirat":
                        personaEstirada(event, inputQueue)

                # There is nobody in the room
                elif person == "no":

                    ac.nobodyintheRoom()

                    #TODO:buscar yayo
                    # The robot looks for the user
                    ac.buscarYayo(event)
                    searchOK = searchForSomeone(event)

                    if searchOK == 'OK':
                        print('\n')
                        print("-" * 100)
                        print("Robot finds the user")
                        print("-" * 100)
                        # Event where the robot only has to inform the user that they occurred
                        if event.event == 'FireAlarm' or event.event == 'Doorbell' or event.event == 'RunningWater' or event.event == 'Rain':
                            er.infoEvent(event, inputQueue)

                        else:
                            er.askIfEventHappened(event, inputQueue)
                    else:
                        print("We can't found anyperson")

                llista.eventRemove(event)
                #el robot se dirige al punto de carga.
                NavegationEnd()

            # el robot no se puede mover
            elif navOK == 'KO':
                llista.eventRemove(event)
                ac.InformRobotCannotMove()
                print("-" * 50, "END TASK", "-" * 50)

            # no he prodido connectar con la nevagacion
            else:
                llista.eventRemove(event)
                print("Finish the task")
                print("-" * 50, "END TASK", "-" * 50)



if __name__ == "__main__":
    main()