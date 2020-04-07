
% Classifier Core IP and port
addr = '127.0.0.1';
port = 8000;
sensorName = 'kitchen';

% If this .m is moved, change the line below. It should point to the Feature
% extraction folder.
addpath('./Feature extraction/');

% Variables
Fs = 44100 ;        % Sampling frequency
nBits = 16 ;        % Sampling accuracy?
nChannels = 1 ;     % Number of channel  1 for mono & 2 for stereo
ID = -1;            % default audio input device
recObj = audiorecorder(Fs,nBits,nChannels,ID);
TimeSave = 1 ;      % Time of recording in sec

stWin = 100e-3;     % short-term window size (in seconds)
stStep = 50e-3;     % short-term window step (in seconds)

mtWin = 0.5;        % mid-term window size (in seconds)
mtStep = 0.1;       % mid-term window step (in seconds)

% convert mt win and step to ratio (compared to the short-term):
mtWinRatio  = round(mtWin  / stStep);
mtStepRatio = round(mtStep / stStep);

%Connect to the server
sock = serverConnect(addr, port, sensorName);

sendErrorCounter = 0;

while true
    
    % Record [Gaëtan & Adria]
    % -----------------------------------Signal recording & saving -------------------------
    
    recordblocking(recObj,TimeSave);     %Synchronous recording from audio device.
    %records for length of time, TimeSave, in seconds;
    %does not return until recording is finished
    
    audioData = getaudiodata(recObj);    %Get the audiodata
    
    % STEP 1: short-term feature extraction:
    stFeatures = stFeatureExtraction(audioData, Fs, stWin, stStep, {'mfcc'});
    
    % STEP 2: mid-term feature extraction:
    %[mtFeatures, st] = mtFeatureExtraction(stFeatures , mtWinRatio, mtStepRatio, '');
    
    size = size(stFeatures, 2);
    %Send audio features (MFCC components)
    for i = 1:size
        
        %TESTING AREA (IGNORE)
        %components = num2str(stFeatures(:,i), "%f");
        %fprintf('Components extracted at %s: \n%s\n',datestr(now,'HH:MM:SS.FFF'),components);
        %result = 1;
        %END OF TESTING AREA
        
        result = serverSendComponents(sock, stFeatures(:,i)); 
        %Check for errors.
        if (result == 0)
            
            fprintf('Error sending component \n');
            %If there are 10 errors in a row, exit.
            sendErrorCounter = sendErrorCounter + 1;
            if sendErrorCounter >= 10
                break;
            end
        else
            sendErrorCounter = 0;
        end
    end
end

serverDisconnect(sock);
disp('Disconnected from Server')