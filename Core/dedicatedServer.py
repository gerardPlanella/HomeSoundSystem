import socket
import numpy as np
from events import event, threadInfo
from classifier import Classifier

DEBUGGING = True

NUM_COMPONENTS = 13

OK = "ok"
KO = "ko"

class Client:
    __slots__ = ['fifo', 'name']

    def __init__(self, name):
       fifo = []
       self.name = name


def sendString(socket, msg):
    socket.sendall(msg.encode())

def receiveString(socket):
    data = socket.recv(1024)
    str_data = data.decode('utf-8')
    str_data = str_data.rstrip()
    return str_data

def getComponentsFromMessage(message):
    str_data = str_data.rstrip()
    if str(str_data) == "disconnect":
         return [0, ""]
    component_str = str_data.split(' ')
    component_str = list(filter(lambda a: a != '', component_str))
    component_str = np.array(component_str)
    components = component_str.astype(np.float)
    return [1, components]


def runDS(threadInfo, client):
    ds_run = True
    classifier = Classifier()
    
    if (DEBUGGING): print("Sensor name: " + client.name + " \n")

    while (threadInfo.running and ds_run):
        if len(client.fifo) > 0:
            component = client.fifo.pop(0)
            [ok, component] = getComponentsFromMessage(component)
            if (not ok):
                if (DEBUGGING): print(client.name + " Client disconnected\n")
                ds_run = False
            else:
                if (DEBUGGING): print("Data received: " + str(component) + "\n")
                if (len(component) != NUM_COMPONENTS and DEBUGGING): print("Incorrect components received")
                classifyComponents(threadInfo, component, client.name)

def classifyComponents(threadInfo, components, name):
    
    [event, confidence] = classifier.predict(components)
    if(event_index != ""):
        event = Event(event, name, confidence)
        threadInfo.addEvent(event)
        return 1
    else:
        return 0

