function [sock, ok] = serverConnect(addr, port, sensorName)
%Connects to the python server and performs handshake
ok = 0;
sock = tcpip(addr, port, 'NetworkRole', 'client');
fopen(sock);

flushinput(sock);

fprintf(sock, sensorName);
resp = fscanf(sock);

if (strcmp(resp, 'ok'))
    ok = 1;
end

end

