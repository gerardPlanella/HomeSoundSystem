#!/usr/bin/env python
# -*- coding: utf-8 -*-
from asyncio import wait
import random
from time import sleep
import cua as c
import threading
import audio as al
import socket

from poseConnection import posseConnection, connected

HOST = '25.120.131.106'  # Standard loopback interface address (localhost)
PORT = 8001        # Port to listen on (non-privileged ports are > 1023)
classLabels = ['Complain', 'FireAlarm', 'BoilingWater', 'GlassBreak', 'Doorbell', 'Fall', 'CutleryFall', 'HeavyBreath', 'Rain', 'Help', 'RunningWater','Silence']
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



def iniciEvent(evento):
    print("The " + evento.event + " event has ocurred and I am going to the " + evento.lloc + " to check what happened.")
    #FET: ecriure frase explicació(julia)
    text = "The " + evento.event + " event has ocurred and I am going to the " + evento.lloc + " to check what happened."
    speak.reproduceText(text)
    return 0

def explicacioDeEvent(evento):
    print("I detected that the "+ evento.event+ " ocurred and I came to check if everything is OK.")
    # FET: ara ja esta a la habitació ha trobat a la persona i li diu pq estroba alla (julia)
    text = "I detected that the "+ evento.event+ " ocurred and I came to check if everything is OK."
    speak.reproduceText(text)
    return 0

def preguntarEstat():
    print("Are you hurt?")
    # FET: Demanar com es troba el yayo (julia), si s'ha fet mal
    text = "Are you hurt?"
    speak.reproduceText(text)
    return 0

def demanarAjuda():
    pass

def preguntaAjuda():
    print("Do you want me to contact someone to help you?")
    text = "Do you want me to contact someone to help you?."
    speak.reproduceText(text)
    return 0


def explicacioSituacioResponsable(evento):
    print("I detected that the ", evento.event, " ocurred at ", evento.timeestamp, " and I went to ", evento.lloc, " to check the situation and I asked for help." )
    text = "I detected that the "+ evento.event+ " ocurred at "+ evento.timeestamp+ " and I went to "+ evento.lloc+ " to check the situation and I asked for help."
    speak.reproduceText(text)
    return 0

def finalProces(evento):
    print("The task related to the ", evento.event, " event is finished and I will return to the resting point.")
    text = "The task reladed to the ", evento.event, " event  is finished and I will return to the resting point."
    speak.reproduceText(text)
    return 0

def retornInici():
    print("I am going to the resting point.")
    text = "I am going to the resting point."
    speak.reproduceText(text)
    return 0

def errorEvent():
    print("A sensor error has occurred.")
    text = "A sensor error has occurred."
    speak.reproduceText(text)
    return 0

def ferCompanyia():
    pass

def analitzaResposta():
    pass

def esperarPersonaPeu():
    pass

def buscarYayo(evento):
    print("I am moving arround the house to find you because I detected that the ", evento.event, " ocurred.")
    text = "I am moving arround the house to find you because I detected that the "+ evento.event+ " ocurred."
    speak.reproduceText(text)
    return 0

def main():
    llista = c.ListaEvents()
    try:
        x = threading.Thread(target=thread_function_SERVERCON, args=(llista,))
        x.start()
    except:
        print("server not connection")
    speak.reproduceText("hello")
    while(True):
        if llista.anyList() != 0:
            print("-" * 1000)
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
                    preguntarEstat()
                    # TODO: acabar interaccio si la persona esta dreta (fer opcions per terminal o random)
                    pose.delete()
                elif pose.getposition() == "sentat":
                    preguntarEstat()
                    # TODO: acabar interaccio si la persona esta sentada (fer opcions per terminal o random)
                    pose.delete()
                elif pose.getposition() == "estirat":
                    preguntarEstat()
                    #TODO: acabar interaccio si la persona esta estirada (fer opcions per terminal o random)
                    pose.delete()
            else:
                print("no hi ha persona")
                pose.delete()
                errorEvent()
                retornInici()
                # TODO:robot es mou (navegation)
                print("moure robot ", event.lloc)
                print("el robot arriba al lloc ", "+" * 100)




if __name__ == "__main__":
    main()