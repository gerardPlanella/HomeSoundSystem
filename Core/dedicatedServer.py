import socket
import numpy as np
#from events import event, threadInfo
import events
import classifier as clsfy

DEBUGGING = True

NUM_COMPONENTS = 13

OK = "ok"
KO = "ko"

INIT_VALUE = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
summary = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
burst = 0

class Client:
    __slots__ = ['fifo', 'name']

    def __init__(self, name):
       self.fifo = []
       self.name = name


def sendString(socket, msg):
    socket.sendall(msg.encode())

def receiveString(socket):
    data = socket.recv(1024)
    str_data = data.decode('utf-8')
    str_data = str_data.rstrip()
    return str_data

def getComponentsFromMessage(message):
    str_data = message.rstrip()
    if str(str_data) == "disconnect":
         return [0, ""]
    component_str = str_data.split(' ')
    component_str = list(filter(lambda a: a != '', component_str))
    component_str = np.array(component_str)
    components = component_str.astype(np.float)
    return [1, components]


def runDS(threadInfo, client):
    ds_run = True
    classifier = clsfy.Classifier()

    if (DEBUGGING): print("Sensor name: " + client.name + " \n")
    burst = 0
    summary = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    while (threadInfo.running and ds_run):
        if len(client.fifo) > 0:
            component = client.fifo.pop(0)
            #print("Message: " + str(component))

            [ok, component] = getComponentsFromMessage(component)
            #print("Components: " + str(component))

            if (not ok):
                #if (DEBUGGING):
                print(client.name + " Client disconnected\n")
                ds_run = False
            else:
                #if (DEBUGGING): print("Data received: " + str(component) + "\n")
                if (len(component) != NUM_COMPONENTS and DEBUGGING): print("Incorrect components received")
                classifyComponents(threadInfo, component, client.name, classifier)

def classifyComponents(threadInfo, components, name, classifier):
    global burst
    classLabels = ['Complain', 'FireAlarm', 'BoilingWater', 'GlassBreak', 'Doorbell', 'Fall', 'CutleryFall', 'HeavyBreath', 'Rain', 'Help', 'RunningWater', 'Silence']
    [event_name, event_index, confidence] = classifier.predict(components)
    if(event_name != ""):
        event = events.Event(event_index, name, confidence)
        threadInfo.addEvent(event)

        summary[event_index] += 1
        burst += 1

        if False:
            print("-"*50)
            print(event_name)
            print(event.time)
            #print(event.location)
            print(event.confidence)

        if (burst == 30):
            burst = 0
            print("-"*50)
            for i in range(len(summary)):
                print(classLabels[i] + ": " + str(summary[i]))
                summary[i] = 0

        return 1
    else:
        return 0
