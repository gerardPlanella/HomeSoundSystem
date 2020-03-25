#Made by Gerard Planella

import socket
import sys
import numpy as np
import time

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 8000        # Port to listen on (non-privileged ports are > 1023)
OK = "ok"
KO = "ko"

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((HOST, PORT))


bytesAddressPair = s.recvfrom(1024)
data = bytesAddressPair[0]
address = bytesAddressPair[1]

sensorName = data.decode('utf-8')
print("Sensor name: " + str(sensorName) +  " Address: " + str(address))
s.sendto(OK.encode(), address)

start = time.time()
n_packets = 0

while True:
    bytesAddressPair = s.recvfrom(1024)
    data = bytesAddressPair[0]
    address = bytesAddressPair[1]
    
    str_data = data.decode('utf-8')
    str_data = str_data.rstrip()
    if str(str_data) == "disconnect":
         s.sendto(OK.encode(), address)
         break
    component_str = str_data.split(' ')
    component_str = list(filter(lambda a: a != '', component_str))
    component_str = np.array(component_str)
    components = component_str.astype(np.float)

    print("Data received: " + str_data + "\n")
    print("Components received: " + str(component_str) + "\n")
    s.sendto(OK.encode(), address)
    n_packets = n_packets + 1

end = time.time()
print("Total time per sample = %s seconds", (start-end)/n_packets)
print("Communication DONE\n")
