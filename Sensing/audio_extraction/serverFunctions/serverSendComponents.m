function serverSendComponents(sock, components)
%Sends MFCC components to python Server
tic
flushinput(sock);
toc
components = num2str(components, "%f");
fprintf(sock, components);

end

