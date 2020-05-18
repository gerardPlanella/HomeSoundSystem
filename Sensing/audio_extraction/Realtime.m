%TODO: Gaetan, when you use ctrl C to finish code the function disconnect
%wont ever execute, look at the onCleanup function of matlab and maybe
%control the errors with try catch clauses

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
ID = -1;            % default audio input device
recObj = audiorecorder(Fs,nBits,nChannels,ID);
TimeSave = 1 ;      % Time of recording in sec

stWin = 500e-3;     % short-term window size (in seconds)
stStep = 125e-3;     % short-term window step (in seconds)

mtWin = 0.5;        % mid-term window size (in seconds)
mtStep = 0.1;       % mid-term window step (in seconds)

% convert mt win and step to ratio (compared to the short-term):
mtWinRatio  = round(mtWin  / stStep);
mtStepRatio = round(mtStep / stStep);

%Connect to the server
%sock = serverConnect(addr, port, sensorName);

connected = true;
disp('Connected to server')
% i = 0;
% audioData_aux = [];

while true
    
    % Record [Gaetan & Adria]
    % -----------------------------------Signal recording & saving -------------------------
    recO
    recordblocking(recObj,TimeSave);     %Synchronous recording from audio device.
    %records for length of time, TimeSave, in seconds;
    %does not return until recording is finished
    
    audioData = getaudiodata(recObj);    %Get the audiodata

    audioData_norm = audioNormalization(audioData, 0.5);
    
%     audioData_aux = [audioData_aux audioData];
%     if i >= 10 
%         break;
%     end
%     
%     i = i + 1;

    
    % STEP 1: short-term feature extraction:
    %stFeatures = stFeatureExtraction(audioData, Fs, stWin, stStep, {'mfcc'});
    
    % STEP 2: mid-term feature extraction:
    %[mtFeatures, st] = mtFeatureExtraction(stFeatures , mtWinRatio, mtStepRatio, '');
    
%     len = size(stFeatures, 2);
%     %Send audio features (MFCC components)
%     for i = 1:len
%         
%         %TESTING AREA (IGNORE)
%         %components = num2str(stFeatures(:,i)', "%f");
%         %disp(components)
%         %result = 1;
%         %END OF TESTING AREA
%         
%         serverSendComponents(sock, stFeatures(:,i)'); 
%     end
end
%ERROR: These two functions will be never executed!!!
serverDisconnect(sock);
disp('Disconnected from Server')


function out = audioNormalization(in, ampMax)
%     Scale speech by its peak value
% 
%     Input Parameters : 
%       in       Input speech
%       ampMax   Expected peak value (0 ~ 1)
%     Output Parameters : enhanced speech  
%       out      Scaled speech
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


function myRecorder = nonBlockingAudioRecorder
      figure;
      hPlot = plot(NaN,NaN);
      sampleRate = 8192;
      myRecorder = audiorecorder(sampleRate,8,1);
      set(myRecorder, 'TimerFcn', @myRecorderCallback, 'TimerPeriod', 1);
      atSecond = 1; 
      record(myRecorder);
      
      function myRecorderCallback(~, ~)
          allSamples = getaudiodata(myRecorder);
          newSamples = allSamples((atSecond - 1) * sampleRate + 1:atSecond * sampleRate);
          xdata = get(hPlot, 'XData');
          ydata = get(hPlot, 'YData');
          if isnan(xdata)
             xdata = linspace(0, atSecond - 1/sampleRate,sampleRate);
             ydata = [];
          else
              xdata = [xdata linspace(atSecond, atSecond + 1 - 1/sampleRate, sampleRate)];
          end
          ydata = [ydata newSamples'];
          set(hPlot, 'XData', xdata, 'YData', ydata);
          atSecond = atSecond + 1;
          if atSecond > 10
              stop(myRecorder);
              delete(myRecorder);
          end
      end
  end