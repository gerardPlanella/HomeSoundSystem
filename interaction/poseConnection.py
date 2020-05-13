import threading
import socket
from multiprocessing.connection import wait
from time import sleep
import random

error_con = 0
connected = 0
HOST = '25.120.137.245'  # Standard loopback interface address (localhost)
PORT = 42069  # Port to listen on (non-privileged ports are > 1023)

yesNo = ["yes", "no"]
pose = ["dret", "estirat", "sentat"]


class posseConnection():
    def __init__(self):
        self.obj = socket.socket()
        self.persona = ""
        self.positions = ""


    def startPoseConnnection(self):
        global error_con
        try:
            self.x = threading.Thread(target=self.thread_function_SERVERCONPOSEprova)
            self.x.start()
        except:
            error_con = 1
            print("not connection pose detenction")

    def thread_function_SERVERCONPOSEprova(self):
        global yesNo
        global pose
        global error_con
        global connected
        error_con = 1
        print("not connection pose detenction")
        sleep(0.5)
        connected = 1

        self.persona = random.choice(yesNo)
        connected = 2

        sleep(10)
        self.positions = random.choice(pose)
        connected = 3

    def thread_function_SERVERCONPOSEdef(self):
        global yesNo
        global pose
        global error_con
        global connected
        error_con = 1
        print("not connection pose detenction")
        sleep(0.5)
        connected = 3



    def thread_function_SERVERCONPOSE(self):
        global error_con
        global connected
        try:
            self.obj.connect((HOST, PORT))
            print('Connected by')
            connected = 1
            self.persona = self.person().decode('ascii')
            print("he rebut",self.persona)
            connected = 2
            self.positions= self.position().decode('ascii')
            print("he rebut", self.positions)
            connected = 3
            self.close()
            self.obj.close()


        except:
            print("not connection pose detenction","*" *50)

            global yesNo
            global pose
            error_con = 1

            sleep(0.5)
            connected = 1
            self.persona = random.choice(yesNo)
            connected = 2
            sleep(5)
            self.positions = random.choice(pose)
            connected = 3


    def person(self):
        self.obj.sendall(b'persona')
        return self.obj.recv(1024)

    def close(self):
        self.obj.sendall(b'close')

    def position(self):
        self.obj.sendall(b'posicion')
        return self.obj.recv(1024)

    def delete(self):
        global connected
        self.x.join()
        connected = 0

    def getconection(self):
        global connected
        return connected

    def getpersona(self):
        return self.persona

    def getposition(self):
        return self.positions

    def setPoseConnection(self, persona, positions):
        self.persona = persona
        self.positions = positions
