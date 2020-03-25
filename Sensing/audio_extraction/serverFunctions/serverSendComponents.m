function [ok] = serverSendComponents(sock, components)
%Sends MFCC components to python Server
ok = 0;
tic
flushinput(sock);
toc
components = num2str(components, "%f");
fprintf(sock, components);
resp = fscanf(sock);

if (strcmp(resp, 'ok'))
    ok = 1;
end

end

