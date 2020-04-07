function serverDisconnect(sock)
%Disconnects from python server

flushinput(sock);
fprintf(sock, "disconnect");
fclose(sock);

end

