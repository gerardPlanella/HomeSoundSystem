function serverSendComponents(sock, components)
%Sends MFCC components to python Server

flushinput(sock);
components = num2str(components, "%f");
disp(components)
fprintf(sock, components);

end

