function [mtFeatures, FileNames,stFeatures] =  featureExtractionDir(dirName, stWin, stStep, mtWin, mtStep, featureStatistics,featureShort)

%
% function [mtFeatures, FileNames,stFeatures] =  featureExtractionDir(dirName, stWin, stStep, mtWin, mtStep, featureStatistics,featureShort,featureShort)
%
% Extracts mid term features for a list of WAV files stored in a given path
% 
% ARGUMENTS:
%  - dirName:           path of the folder that contains the WAV files
%  - stWin, stStep:     short-term window size and step (seconds)
%  - mtWin, mtStep:     mid-term window size and step (seconds)
%  - featureStatistics: list (cell array) of mid term statistics, within 
%                       {'mean','median','std','stdbymean','max','min',
%                       'meanNonZero','medianNonZero'.
%  - featureShort: list (cell array) of short term features, within {'ZCR',
%                       'energy','enEntropy','specCentroid','specSpread',
%                       'specEntropy','specFlux','specRolloff','mfcc',
%                       'harmRatio','f0','chromaVec'}
%
% RETURNS:
%  - mtFeatures:       cell array whose elements are feature matrices 
%                       e.g., mtFeatures{10} contains the mid-term 
%                       feature matrix of the 10th file in the given
%                       directory +++
%  - stFeatures:       cell array whose elements are feature matrices 
%                       e.g., stFeatures{10} contains the short-term 
%                       feature matrix of the 10th file in the given
%                       directory +++ 
%  - FileNames:         cell array that contains the full paths of the 
%                       WAV files in the provided folder
% 
% (c) 2014 T. Giannakopoulos, A. Pikrakis

D = dir([dirName filesep '*.wav']);
stFeatures = cell(1,length(D));
for i=1:length(D)       % for each WAV file
    disp(['Feature extraction for file %50s\n', D(i).name])
    curName = [dirName filesep D(i).name];    
    FileNames{i} = curName;  % get current filename
    % extract mid-term features:
    [midFeatures, Centers, stFeaturesPerSegment,stFeat] = ...
        featureExtractionFile(curName, stWin, stStep, mtWin, mtStep, featureStatistics,featureShort)
    mtFeatures{i} = midFeatures;
    stFeatures{i} = stFeat;
end
