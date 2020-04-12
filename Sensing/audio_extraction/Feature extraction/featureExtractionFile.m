function [midFeatures, Centers, stFeaturesPerSegment,stFeatures] = ...
    featureExtractionFile(fileName, stWin, stStep, mtWin, mtStep, featureStatistics,featureShort)

% function [midFeatures, Centers, stFeaturesPerSegment] = ...
%    featureExtractionFile(fileName, stWin, stStep, mtWin, mtStep, ...
%    featureStatistics,featureShort)
%
% This function reads a wav file and computes 
% audio feature statitstics on a mid-term basis.
%
% ARGUMENTS:
% - fileName:           the name of the input audio file
% - stWin:              short-term window size (in seconds)
% - stStep:             short-term window step (in seconds)
% - mtWin:              mid-term window size (in seconds)
% - mtStep:             mid-term window step (in seconds)
% - featureStatistics:  list of statistics to be computed (cell array)
% - featureShort: list (cell array) of short term features, within {'ZCR',
%                       'energy','enEntropy','specCentroid','specSpread',
%                       'specEntropy','specFlux','specRolloff','mfcc',
%                       'harmRatio','f0','chromaVec'}
% -stFeatures:          matrix of short-term features
% RETURNS
% - midFeatures         [numOfFeatures x numOfMidTermWins] matrix 
%                       (each collumn represents a mid-term feature vector)
% - Centers:            representive centers for each 
%                       mid-term window (in seconds)
% - stFeaturesPerSegment cell that contains short-term feature sequences
%
% (c) 2014 T. Giannakopoulos, A. Pikrakis

% convert mt win and step to ratio (compared to the short-term):
mtWinRatio  = round(mtWin  / stStep);
mtStepRatio = round(mtStep / stStep);

readBlockSize = 60; % one minute block size:

% get the length of the audio signal to be analyzed:
%[a, fs] = audioread(fileName, 'size');
%numOfSamples = a(1);
[info] = audioinfo(fileName);
numOfSamples = info.TotalSamples;
fs = info.SampleRate;

BLOCK_SIZE = round(readBlockSize * fs);
curSample = 1;
count = 0;
midFeatures = [];
Centers = [];
stFeaturesPerSegment = {};
stFeatures = [];

while (curSample <= numOfSamples) % while the end of file has not been reahed
    % find limits of current block:
    N1 = curSample;
    N2 = curSample + BLOCK_SIZE - 1;
    if (N2>numOfSamples)
        N2 = numOfSamples;
    end
    
    %tempX = wavread(fileName, [N1, N2]);        
    tempX = audioread(fileName, [N1, N2]);
    
    % STEP 1: short-term feature extraction:
    Features = stFeatureExtraction(tempX, fs, stWin, stStep,featureShort);
       
    % STEP 2: mid-term feature extraction:
    [mtFeatures, st] = mtFeatureExtraction(...
       Features, mtWinRatio, mtStepRatio, featureStatistics);
    
    for (i=1:length(st)) 
        stFeaturesPerSegment{end+1} = st{i}; 
    end
    Centers = [Centers readBlockSize * count + (0:mtStep:(N2-N1)/fs)];
    midFeatures = [midFeatures mtFeatures];
    
    stFeatures = [stFeatures Features];
    
    % update counter:
    curSample = curSample + BLOCK_SIZE;
    count = count + 1;    
end
if (length(Centers)==1)
    Centers = (numOfSamples / fs) / 2;
else
    C1 = Centers(1:end-1);
    C2 = Centers(2:end);
    Centers = (C1+C2) / 2;
end

if (size(midFeatures,2)>length(Centers))
    midFeatures = midFeatures(:, 1:length(Centers));
end

if (size(midFeatures,2)<length(Centers))
    Centers = Centers(:, 1:size(midFeatures,2));
end
