import socket
import threading
import dedicatedServer
#from events import event, threadInfo
import events
import eventProcessor as ep
import numpy as np

## TODO: Make Client class

HOST = '25.120.131.106'#'127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 8000         # Port to listen on (non-privileged ports are > 1023)

sensorNames = ['kitchen', 'living_room', 'bath_room', 'bed_room']
sensorThreads = []

threadInfo = events.threadInfo()
client_streams = {}


def main():

    eventProcessor = threading.Thread(target = ep.eventProcessorMain, args = (threadInfo, ))
    eventProcessor.start()

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((HOST, PORT))

    print("Server configured")
    accumulatedNum = 0
    accumulator = []

    try:
        while True:
            bytesAddressPair = sock.recvfrom(1024)
            data = bytesAddressPair[0]
            address = bytesAddressPair[1]

            #print("Paquet received")

            if (address in client_streams):
                dataaux = str(data.decode('ascii'))
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

                accumulatedNum += len(component_str)
                for v in component_str: accumulator.append(v)

                isFinal = (accumulatedNum >= 520)

                #print("New message: " + str(component_str))
                #print("Msg lenght: " + str(accumulatedNum))
                #print("Is final: " + str(isFinal))

                if (isFinal): accumulatedNum = 0

                client_streams[address].fifo.append(dataaux)
            else:
                #TODO: Remove OK and KO and Disconnect from Matlab Client
                client = dedicatedServer.Client(data.decode('ascii'))
                client_streams.update({address : client})

                #print_lock.acquire()
                print("Connected to :", address)
                sensor = threading.Thread(target = dedicatedServer.runDS, args=(threadInfo, client, ))
                sensor.start()
                sensorThreads.append(sensor)

    except KeyboardInterrupt:
        threadInfo.setRun(False)
        eventProcessor.join()
        for th in sensorThreads:
            th.join()

if __name__ == "__main__":
    main()
    print("Core Terminated\n")
