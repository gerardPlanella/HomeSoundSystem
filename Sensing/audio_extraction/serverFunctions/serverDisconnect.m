function [ok] = serverDisconnect(sock)
%Disconnects from python server
ok = 0;
order = 'disconnect';

flushinput(sock);

fprintf(sock, order);
resp = fscanf(sock);

if (strcmp(resp, 'ok'))
    ok = 1;
    fclose(sock);
end

end

