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
            self.x = threading.Thread(target=self.thread_function_SERVERCONPOSE)
            self.x.start()
            if error_con == 1:
                print("not connection pose detenctiones -- Estart debug")
            else:
                error_con = 0
            return True
        except:
            error_con = 1
            print("not connection pose detenction")
            return False


    def thread_function_SERVERCONPOSE(self):
        global error_con
        try:
            error_con = 0
            self.obj.connect((HOST, PORT))
            print('Connected by pose ')

        except:
            error_con = 1
            print("not connection pose detenction")

        return not error_con


    def person(self):
        try:
            self.obj.sendall(b'persona')
            return self.obj.recv(1024).decode('ascii')
        except:
            return "no"

    def close(self):
        try:
            self.obj.sendall(b'close')
            self.obj.close()
        except:
            pass

    def position(self):
       try:
            self.obj.sendall(b'posicion')
            return self.obj.recv(1024).decode('ascii')
       except:
            return random.choice(pose)


    def delete(self):
        global error_con
        global connected
        #self.x.join()
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
