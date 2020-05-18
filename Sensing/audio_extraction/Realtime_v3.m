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
TimeSave = 1 ;      % Time of recording in sec

stWin  = 50e-3;         % short-term window size (in seconds)
stStep = 25e-3;         % short-term window step (in seconds)

spectrogram_win  = 1 ;     %(in seconds)
spectrogram_step = 250e-3; %(in seconds)

nSpect_win = spectrogram_win / stStep;
nSpect_step = spectrogram_step / stStep; 



ncmp_spec = nSpect_win * 13;



%Connect to the server
sock = serverConnect(addr, port, sensorName);

connected = true;
disp('Connected to server')

realtime_audio(sock, Fs, stWin, stStep, TimeSave, nBits, nSpect_win, nSpect_step);

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


function realtime_audio(sock, Fs, stWin, stStep, TimeSave, nBits, nSpect_win, nSpect_step)
    deviceReader = audioDeviceReader(Fs, floor(Fs * (TimeSave + 0.25)), 'NumChannels', 1);
    setup(deviceReader)
    divisor = 20;
%    figure;
%    exit_var = plot(NaN, NaN);
%    drawnow

%      try
        while true
            %set(exit_var, 'XData', []);
            [audioData, nOverrun] = record(deviceReader);
            %audioData = audioNormalization(audioData, 0.5);
            stFeatures = stFeatureExtraction(audioData, Fs, stWin, stStep, {'mfcc'});
            lost = length(stFeatures) - nSpect_win; 
            nSpect = floor((length(stFeatures) / nSpect_step) - nSpect_win/nSpect_step + 1);
            current = 1;
            
            for i = 1:nSpect
                spect = stFeatures(:, current:(current + nSpect_win - 1));
                spect = reshape(spect, 1, []);
                current_2 = 0;
                for j = 1:divisor
                    serverSendComponents(sock, spect(:, (current_2 + 1) : current_2 + (nSpect_win * 13/divisor)));
                    pause(0.02);
                    current_2 = current_2 + (nSpect_win * 13/divisor);
                end
                current = current + nSpect_step;           
            end
        end
%     catch
%         release(deviceReader)
%         serverDisconnect(sock);
%         disp("STOP");
%     end    
end