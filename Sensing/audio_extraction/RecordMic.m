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
nonBlockingAudioRecorder();
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
          end
      end
  end
