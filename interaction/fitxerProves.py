
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
from poseConnection import posseConnection

classLabels = ['Complain', 'FireAlarm', 'BoilingWater', 'GlassBreak', 'Doorbell', 'Fall', 'CutleryFall', 'HeavyBreath', 'Rain', 'Help', 'RunningWater','Silence']


def thread_function_pravaTotesFuncions(llista):
    print("prova totes les funcions")

    e = c.event("garden", 0, "2020-04-23 20:11:20.728069", float(0.98))
    llista.appendEvent(e)
    sleep(1)
    e1 = c.event("bedroom", 1, "2020-04-23 20:11:20.728069", float(0.98))
    llista.appendEvent(e1)
    sleep(1)
    e2 = c.event("kitchen", 2, "2020-04-23 20:11:20.728069", float(0.98))
    llista.appendEvent(e2)
    sleep(1)
    e3 = c.event("dining room", 3, "2020-04-23 20:11:20.728069", float(0.98))
    llista.appendEvent(e3)
    sleep(1)
    e4 = c.event("hall", 4, "2020-04-23 20:11:20.728069", float(0.98))
    llista.appendEvent(e4)
    sleep(1)
    e5 = c.event("bedroom", 5, "2020-04-23 20:11:20.728069", float(0.98))
    llista.appendEvent(e5)
    sleep(1)
    e6 = c.event("kitchen", 6, "2020-04-23 20:11:20.728069", float(0.98))
    llista.appendEvent(e6)
    sleep(1)
    e7 = c.event("bedroom", 7, "2020-04-23 20:11:20.728069", float(0.98))
    llista.appendEvent(e7)
    sleep(1)
    e8 = c.event("garden", 8, "2020-04-23 20:11:20.728069", float(0.98))
    llista.appendEvent(e8)
    sleep(1)
    e9 = c.event("hall", 0, "2020-04-23 20:11:20.728069", float(0.98))
    llista.appendEvent(e9)
    sleep(1)
    e10 = c.event("bathroom", 10, "2020-04-23 20:11:20.728069", float(0.98))
    llista.appendEvent(e10)
    sleep(1)

def thread_function_prava3funcionsIgualsalMateixTemps(llista):
    e10 = c.event("bathroom", 10, "2020-04-23 20:11:20.728069", float(0.98))
    llista.appendEvent(e10)
    e10 = c.event("bathroom", 10, "2020-04-23 20:11:20.728069", float(0.7))
    llista.appendEvent(e10)
    e10 = c.event("bathroom", 10, "2020-04-23 20:11:20.728069", float(0.4))
    llista.appendEvent(e10)

def poseConPersonDret():
    pose = posseConnection()
    pose.setPoseConnection("yes","dret")
    return pose

def poseConPersonEstirada():
    pose = posseConnection()
    pose.setPoseConnection("yes","estirat")
    return pose

def poseNoPerson():
    pose = posseConnection()
    pose.setPoseConnection("no","")
    return pose



