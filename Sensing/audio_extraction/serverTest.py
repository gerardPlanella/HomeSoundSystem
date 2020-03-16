import socket
import json
import sys
import numpy 

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 8000        # Port to listen on (non-privileged ports are > 1023)
OK = "ok"
KO = "ko"


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
print("Waiting for connection\n")
s.listen()
conn, addr = s.accept()
print('Connected by', addr)
data = conn.recv(1024)
if not data:
    conn.sendall(KO.encode())
    sys.exit()

sensorName = data.decode('utf-8')
print("Sensor name: " + sensorName)
conn.sendall(OK.encode())

while True:
    data = conn.recv(1024)
    str_data = data.decode('utf-8')
    str_data = str_data.rstrip()
    if str(str_data) == "disconnect":
        conn.sendall(OK.encode())
        break
    component_str = str_data.split(' ')
    component_str = list(filter(lambda a: a != '', component_str))
    component_str = np.array(component_str)
    components = component_str.astype(np.float)

    print("Data received: " + str_data + "\n")
    print("Components received: " + str(component_str) + "\n")
    conn.sendall(OK.encode())

print("Communication DONE\n")
       