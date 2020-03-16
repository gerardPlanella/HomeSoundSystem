import socket
import threading
import dedicatedServer

## TODO: Make Client class

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 8000         # Port to listen on (non-privileged ports are > 1023)

sensorNames = ['kitchen', 'living_room', 'bath_room', 'bed_room']
sensorThreads = []

threadInfo = threadInfo()

class threadInfo():
    __slots__ = ["running"]

    def __init__(self):
        self.running = True

    def setRun(self, running):
        self.running = running
    def getRun(self):
        return self.running


def main():

    eventProcessor = threading.Thread(target = eventProcessing, args = (threadInfo, ))
    eventProcessor.start()

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((HOST, PORT))
    sock.listen(5)

    try:
        while True:
            client, addr = sock.accept()
            print_lock.acquire()
            print("Connected to :", addr[0])
            sensor = threading.Thread(target = runDS, args=(threadInfo, client, ))
            sensor.start()
            sensorThread.append(sensor)

    except KeyboardInterrupt:
        ## TODO: disconnect from sensors
        threadInfo.setRun(False)
        eventProcessor.join()
        for th in sensorThreads:
            th.join()

if __name__ == "__main__":
    main()
    print("Core Terminated\n")
