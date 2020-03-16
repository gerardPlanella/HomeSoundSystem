import socket
from _thread import *
import threading

## TODO: Make Client class

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 8000         # Port to listen on (non-privileged ports are > 1023)

sensorNames = ['kitchen', 'living_room', 'bath_room', 'bed_room']

def startThread():
    x = threading.Thread(target = existenceReminder, args = (status, ))
    x.start()
    return x


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((HOST, PORT))
    sock.listen(5)

    try:
        while True:
            client, addr = sock.accept()
            print_lock.acquire()
            print("Connected ")


    except KeyboardInterrupt:
        ## TODO: disconnect from sensors
        print("Core Terminated\n")


if __name__ == "__main__":
    main()
