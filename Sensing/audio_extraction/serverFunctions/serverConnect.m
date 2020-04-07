function [sock] = serverConnect(addr, port, sensorName)
%Connects to the python server
sock = udp(addr, port);
fopen(sock);

flushinput(sock);

fprintf(sock, sensorName);

end

