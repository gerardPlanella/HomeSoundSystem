% Classifier Core IP and port
addr = '25.120.131.106';
port = 8000;
sensorName = 'kitchen';

% If this .m is moved, change the line below. It should point to the Feature
% extraction folder.
addpath('./Feature extraction/');
addpath('./serverFunctions/');

% Variables
Fs = 44100 ;        % Sampling frequency
nBits = 16 ;        % Sampling accuracy?
nChannels = 1 ;     % Number of channel  1 for mono & 2 for stereo
TimeSave = 0.5 ;      % Time of recording in sec

stWin = 100e-3;     % short-term window size (in seconds)
stStep = 50e-3;     % short-term window step (in seconds)

mtWin = 0.5;        % mid-term window size (in seconds)
mtStep = 0.1;       % mid-term window step (in seconds)

% convert mt win and step to ratio (compared to the short-term):
mtWinRatio  = round(mtWin  / stStep);
mtStepRatio = round(mtStep / stStep);

%Connect to the server
sock = serverConnect(addr, port, sensorName);

connected = true;
disp('Connected to server')

realtime_audio(sock, Fs, stWin, stStep, TimeSave, nBits);

function out = audioNormalization(in, ampMax)
    out = zeros(length(in),1);
    if( ampMax > 1 || ampMax < 0 )
        fprintf('(ampMax) out of bound.');
    else
        if max(in) > abs(min(in))
            out = in*(ampMax/max(in));
        else
            out = in*((-ampMax)/min(in));
        end
    end
end


function realtime_audio(sock, Fs, stWin, stStep, TimeSave, nBits, sampleRate)

    deviceReader = audioDeviceReader(Fs, Fs * TimeSave, 'NumChannels', 1);
    setup(deviceReader)
    figure;
    exit_var = plot(NaN, NaN);
    drawnow
    
    try

        while true
            set(exit_var, 'XData', []);
            [audioData, nOverrun] = record(deviceReader);
            audioData = audioNormalization(audioData, 0.5);

            stFeatures = stFeatureExtraction(audioData, Fs, stWin, stStep, {'mfcc'});
            
            len = size(stFeatures, 2);
            for i = 1:len
                stFeatures(:,i)'
                serverSendComponents(sock, stFeatures(:,i)');
            end
        end
    catch
        release(deviceReader)
        serverDisconnect(sock);
        disp("STOP");
    end    
end
