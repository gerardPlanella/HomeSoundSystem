import socket
import numpy as np

DEBUGGING = True

OK = "ok"
KO = "ko"

def sendString(socket, msg):
    socket.sendall(msg.encode())

def receiveString(socket):
    data = socket.recv(1024)
    str_data = data.decode('utf-8')
    str_data = str_data.rstrip()
    return str_data

def getComponentsFromMessage(msg):
    msg = str_data.split(' ')
    msg = list(filter(lambda a: a != '', msg))
    msg = np.array(msg)
    return msg.astype(np.float)

#TODO: 
def getComponentsFromMessage(message):
    return

#TODO: reforçar seguretat en cas de detectar algun error
def runDS(threadInfo, socket):
    data = socket.recv(1024)
    if not data:
        sendString(socket, KO)
        return

    location = data.decode('utf-8')
    if (DEBUGGING): print("Sensor name: " + sensorName)

    sendString(socket, OK)

    while (threadInfo.running):
        message = receiveString(socket)

        if (message == "disconnect"):
            sendString(OK)
            break

        components = getComponentsFromMessage(message)

        if (DEBUGGING): print("Data received: " + message + "\n")
        if (DEBUGGING):print("Components received: " + str(components))
        classifyComponents()

        sendString(socket, OK)
