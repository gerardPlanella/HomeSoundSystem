%% Create a audiorecorder object to gather data from the mic.
Fs = 44100 ; 
nBits = 16 ; 
nChannels = 2 ; 
ID = -1; % default audio input device 
recObj = audiorecorder(Fs,nBits,nChannels,ID);

%% Record 5 Seconds of audio
disp('Start speaking.')

recordblocking(recObj,5);
disp('End of Recording.');

%% Play the audio recorded.
play(recObj);


%%
% Define callbacks to show when
% recording starts and completes.
myVoice.StartFcn = 'disp(''Start speaking.'')';
myVoice.StopFcn = 'disp(''End of recording.'')';

record(myVoice);

doubleArray = getaudiodata(myVoice);
plot(doubleArray);
title('Audio Signal (double)');

%play(myVoice);



%% sasd

myVoice = audiorecorder;

maxValue = 0;
for i = 1:n
    recordblocking(myVoice, 0.1);
    data = getaudiodata(myVoice);
    m = mean(data);
    if m > maxValue
        maxValue = m
    end
    if m > 0.005
        plot(data,'-b');
        drawnow;
    end
end

%% 

scope = dsp.SpectrumAnalyzer;
scope(getaudiodata(recObj));

%%

cleanupObj = onCleanup(@cleanMeUp);
nonBlockingAudioRecorder();

% fires when main function terminates
function cleanMeUp()
    % saves data to file (or could save to workspace)
    disp("HI welcome to chillis.")
    delete(myRecorder)
end
    
function myRecorder = nonBlockingAudioRecorder
      figure;
      hPlot = plot(NaN,NaN);
      Fs = 44100 ;        % Sampling frequency
      nBits = 16 ;        % Sampling accuracy?
      nChannels = 1 ;     % Number of channel  1 for mono & 2 for stereo
      ID = -1;            % default audio input device
      atSecond = 1
      myRecorder = audiorecorder(Fs, nBits, nChannels, ID);
      TimeSave = 1 ;      % Time of recording in sec
      set(myRecorder, 'TimerFcn', @myRecorderCallback, 'TimerPeriod', TimeSave);
      record(myRecorder);
      
      function myRecorderCallback(~, ~)
          try
              allSamples = getaudiodata(myRecorder);
              disp(size(allSamples))

              newSamples = allSamples((atSecond - 1) * Fs + 1:atSecond * Fs);
              xdata = get(hPlot, 'XData');
              ydata = get(hPlot, 'YData');
              if isnan(xdata)
                 xdata = linspace(0, atSecond - 1/Fs,Fs);
                 ydata = [];
              else
                  xdata = [xdata linspace(atSecond, atSecond + 1 - 1/Fs, Fs)];
              end
              ydata = [ydata newSamples'];
              set(hPlot, 'XData', xdata, 'YData', ydata);

              atSecond = atSecond + 1;

              if atSecond > 10
                stop(myRecorder)
                delete(myRecorder)
              end
          catch
               stop(myRecorder)
                delete(myRecorder)
          end
          
      end
  end
