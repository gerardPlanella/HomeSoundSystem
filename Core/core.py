import socket
import threading
import dedicatedServer
#from events import event, threadInfo
import events
import eventProcessor as ep

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

    try:
        while True:
            bytesAddressPair = sock.recvfrom(1024)
            data = bytesAddressPair[0]
            address = bytesAddressPair[1]

            #print("Paquet received")

            if (address in client_streams):
                client_streams[address].fifo.append(data.decode('utf-8'))
            else:
                #TODO: Remove OK and KO and Disconnect from Matlab Client
                client = dedicatedServer.Client(data.decode('utf-8'))
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
