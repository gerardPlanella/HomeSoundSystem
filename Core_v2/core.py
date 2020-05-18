import socket
import threading
import dedicatedServer
#from events import event, threadInfo
import events
import eventProcessor as ep
import numpy as np
from keras.models import model_from_json
import classifier
import time

## TODO: Make Client class

HOST = '25.120.131.106'#'127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 8000         # Port to listen on (non-privileged ports are > 1023)

sensorNames = ['kitchen', 'living_room', 'bath_room', 'bed_room']
sensorThreads = []

threadInfo = events.threadInfo(classifier.load_trained_model("model_CNN.json", "modelCNN.hdf5"))
client_streams = {}


def main():

    eventProcessor = threading.Thread(target = ep.eventProcessorMain, args = (threadInfo, ))
    eventProcessor.start()

    print("Server configured")
    client = dedicatedServer.Client('null')

    try:
        socket_listener_thread = threading.Thread(target = socket_listener, args = (threadInfo, client, ))
        socket_listener_thread.start()

        print("Waiting for connection")
        while threadInfo.running == False: time.sleep(.5)

        print("Starting runDS")
        dedicatedServer.runDS(threadInfo, client)

    except KeyboardInterrupt:
        threadInfo.setRun(False)
        eventProcessor.join()

def socket_listener(threadInfo, client):

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((HOST, PORT))

    accumulatedNum = 0
    accumulator = []

    while True:
        bytesAddressPair = sock.recvfrom(1024)
        data = bytesAddressPair[0]
        address = bytesAddressPair[1]

        if (address in client_streams):
            dataaux = str(data.decode('ascii'))
            if (dataaux == "disconnect"):
                client_streams[address].fifo.append(dataaux)

            if ("\n" in dataaux): dataaux = dataaux[:-1]

            component_str = dataaux.split(' ')
            component_str = list(filter(lambda a: a != '', component_str))
            component_str = np.array(component_str)
            for i in range(len(component_str)):
                ind = component_str[i].find("-", 2)
                if (ind == -1):
                    ind = component_str[i].find("-", 0)
                    if (ind == 0 or ind == -1):
                        continue
                num1 = component_str[i][0:ind-1]
                num2 = component_str[i][ind:]
                component_str[i] = num1

                component_str = np.insert(component_str, i+1, num2)

            component_str = component_str.astype(np.float)
            if (len(component_str) != 26): print("\n\nEsta pasando ermano\n\n")

            accumulatedNum += len(component_str)
            for v in component_str: accumulator.append(v)

            if (accumulatedNum >= 520):
                accumulatedNum = 0
                client_streams[address].fifo.append(accumulator)
                accumulator = []

            elif (accumulatedNum < 520 and accumulatedNum > 494):
                accumulatedNum = 0
                accumulator = []
                print("[Error] Packet discarded because of corrupted data")

        else:
            #client = dedicatedServer.Client(data.decode('ascii'))
            client.name = data.decode('ascii')
            client_streams.update({address : client})
            threadInfo.running = True

            print("Client connected: " + client.name)


if __name__ == "__main__":
    main()
    print("Core Terminated\n")
