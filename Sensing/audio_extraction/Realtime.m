% Variables [Gaëtan & Adria]
Fs = 44100 ; % Sampling frequency
nBits = 16 ; % Sampling accuracy? 
nChannels = 2 ; % Number of channel  1 for mono & 2 for stereo
ID = -1; % default audio input device 
recObj = audiorecorder(Fs,nBits,nChannels,ID);
TimeSave = 1 ; % Time of recording in sec

FilesSaved = '.\Recorded_SOUND\RealtimeSample.wav';
dirName    = '.\Recorded_SOUND';
path_feature_extraction = 'C:\Users\user\Documents\ecole\Master 2\Project Robotica\Extracted_SOUND';
classLabels = {'RealtimeSample'};

stWin = 100e-3;      % short-term window size (in seconds)
stStep = 50e-3;      % short-term window step (in seconds) 

mtWin = 0.5;         % mid-term window size (in seconds)
mtStep = 0.1;        % mid-term window step (in seconds) 

N_AUDIOS = 10;       % Number of frequential component wanted 

addr = '127.0.0.1';  % Address of echo server tested
port = 8000;


addpath('./Feature extraction/'); 

% Record [Gaëtan & Adria]
%%-----------------------------------Signal recording & saving -------------------------
recordblocking(recObj,TimeSave);     %Synchronous recording from audio device.
                                     %records for length of time, TimeSave, in seconds;
                                     %does not return until recording is finished
                                     
audioData = getaudiodata(recObj);    %Get the audiodata

% convert mt win and step to ratio (compared to the short-term):
mtWinRatio  = round(mtWin  / stStep);
mtStepRatio = round(mtStep / stStep);

% STEP 1: short-term feature extraction:
stFeatures = stFeatureExtraction(audioData, Fs, stWin, stStep, {'mfcc'});

% STEP 2: mid-term feature extraction:
[mtFeatures, st] = mtFeatureExtraction(...
    stFeatures , mtWinRatio, mtStepRatio, '');