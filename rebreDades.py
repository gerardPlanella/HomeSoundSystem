from cua import *
import socket
import logging
import threading
import time

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

def llegirSoket(s, caracter):
    request_line = ""
    while not request_line.endswith(caracter):
        request_line += s.recv(1)
    request_line = request_line[:-1]
    return request_line

def thread_function():
    while(True):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((HOST, PORT))
            s.listen()
            conn, addr = s.accept()
            with conn:
                print('Connected by', addr)
                while True:
                    data = []
                    data[0] = llegirSoket(s, '%')
                    data[1] = llegirSoket(s, '%')
                    data[2] = llegirSoket(s, '\n')
                    llista = ListaEvents()
                    # Mirar si el event esta repentit, p
                    llista.appendEvent(event(data[1], data[1], data[2], 0.9))
                    if not data:
                        break
                    conn.sendall("ok")

def main():
    x = threading.Thread(target=thread_function)
    x.start()
    while(True):
        llista = ListaEvents()
        if llista.anyList():
            event = llista.popEvent()
            print("moure robot ", event.lloc)



if __name__ == "__main__":
    main()
