import db
import socket
import time

HOST = '25.120.131.106'  # Standard loopback interface address (localhost)
PORT = 8001         # Port to listen on (non-privileged ports are > 1023)

def sendString(socket, msg):
    socket.sendall(msg.encode())

def eventProcessorMain(threadInfo):
    print("Connecting to robot")

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((HOST, PORT))
    sock.listen(5)

    client = 0

    try:
        client, addr = sock.accept()
        #print_lock.acquire()
        print("[ETP] Connected to Robot in @ :" + addr[0])
    except Exception as e:
        print("error connecting to robot")
        print(e)

    database = db.HomeSoundSystemDB()

    while (threadInfo.running):

        while (threadInfo.nEvents() == 0 or not threadInfo.running):
            time.sleep(.1)

        if (not threadInfo.running): break

        event = threadInfo.getEvent()

        print("New event: " + event.type)

        robotHasToBeNotified = True
        if (robotHasToBeNotified):
            sendString(sock, event.location + "%" + str(event.type) + "%" + str(event.time))

        database.addLog(event)

    closeDB()
