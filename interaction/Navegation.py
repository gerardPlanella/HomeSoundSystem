import threading
import socket
import actions as ac

from multiprocessing.connection import wait
from time import sleep
import random

HOST = '25.120.137.245'  # Standard loopback interface address (localhost)
PORT = 42069  # Port to listen on (non-privileged ports are > 1023)


error_con = 0

okko = ["OK", "KO"]
class navegation():
    def __init__(self):
        self.obj = socket.socket()


    def startNavegation(self):
        global error_con
        # Nos connectamos con el modulo de navegacion
        try:
            self.x = threading.Thread(target=self.thread_function_SERVERCONNAV)
            self.x.start()
            error_con = 0
            return True
        except:
            error_con = 1
            print("not connection navegation")
            return False

    def thread_function_SERVERCONNAV(self):
        global error_con
        try:
            self.obj.connect((HOST, PORT))
            print('Connected by')
            error_con = 0
        except:
            error_con = 1
            print("not connection navegation---> Start simulation")
            return False

    #le pedimos al robot que gire
    def turn(self):
        try:
            self.obj.sendall(b'turn')
            return self.obj.recv(1024).decode('ascii')
        except:
            return random.choice(okko)


    # le pedimos al robot que vaya a una sala
    def goSomewhere(self, sitio):
        try:
            self.obj.sendall(b'go')
            self.obj.sendall(sitio.endecode('ascii'))
            return self.obj.recv(1024).decode('ascii')
        except:
            return random.choice(okko)

    # cerramos connexion con la navegación
    def close(self):
        global error_con
        global okko
        try:
            self.obj.sendall(b'close')
            self.obj.close()
            self.x.join()
        except:
            self.x.join()