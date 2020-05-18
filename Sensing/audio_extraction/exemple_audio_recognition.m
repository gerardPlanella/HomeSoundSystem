%% Config 

%Classifier Core IP and port
addr = '127.0.0.1'; %localhost for now
port = 8000;
sensorName = 'kitchen';

%active_dataset  = 'soundscapes';
active_dataset  = 'PolishedDataset';
%active_dataset = 'TestData';

% Directori a on tenim les dades etiquetades
dirName = active_dataset;
% Path la carpeta amb les funcions d'extraccio de caracteristiques (MFCC)
path_feature_extraction = './Feature extraction';

path_server_functions = './serverFunctions';


% Simulation parameters
stWin  = 100e-3;         % short-term window size (in seconds)
stStep = 50e-3;         % short-term window step (in seconds)
%classLabels = {'Bus','Car','CityPark','Classroom','Countryside','Crowd','Factory','Library','Market_pedest','Office','Seaside','Stadium','Station','Traffic','Train'};
classLabels = {'Complain', 'FireAlarm', 'WaterBoiling', 'GlassBreak', 'Doorbell', 'Fall', 'CutleryFall', 'HeavyBreath', 'Rain', 'Help', 'RunningWater', 'Silence'};
knn_K = 3;              % KNN parameter K value
%--------------------------------------------------------------------------
addpath(path_feature_extraction);
addpath(path_server_functions);
% Parametrize dirName WAV files, and obtain feature parameters in
% mtFeatures cell array and filenames in FileNames cell array
disp('Parsing directory ...')
[~, FileNames,stFeatures] =  featureExtractionDir(dirName, stWin, stStep, 1.25, 0.25, '',{'mfcc'});

% Adaptem els atributs d'audio a les especificacions de la llibreria de ML
% --> features: atributs (N files = trames)x(L = 13 atributs MFCC)
% --> classIndex: classe de cada trama en forma de n�mero enter (N files = trames)x1
features = [];
classIndex = [];
for n = 1:length(FileNames)
    features = [features;transpose(stFeatures{n})];
    index = classindex(FileNames{n},classLabels);
    classIndex = [classIndex;index*ones(size(stFeatures{n},2),1)];
end

nExamples = size(features,1);
nFeatures = size(features,2);
nclass = length(classLabels);

% Aleatoritzem les dades per assegurar que tindrem exemples de totes les
% classes en les particions d'entrenament i test
mapping = randperm(nExamples);
features_rand = features(mapping,:);
classIndex_rand = classIndex(mapping,:);

disp('Done!')

%% Extract Directory Components to Spectrograms
path_feature_extraction = './Feature extraction';
path_server_functions = './serverFunctions';

addpath(path_feature_extraction);
addpath(path_server_functions);

%active_dataset  = 'soundscapes';
active_dataset  = 'PolishedDataset';
%active_dataset = 'TestData';

% Directori a on tenim les dades etiquetades
dirName = active_dataset;
% Path la carpeta amb les funcions d'extraccio de caracteristiques (MFCC)
path_feature_extraction = './Feature extraction';

path_server_functions = './serverFunctions';

spectrogram_win  = 1 %(in seconds)
spectrogram_step = 250e-3 %(in seconds)

% Simulation parameters
stWin  = 50e-3;         % short-term window size (in seconds)
stStep = 25e-3;         % short-term window step (in seconds)
%classLabels = {'Bus','Car','CityPark','Classroom','Countryside','Crowd','Factory','Library','Market_pedest','Office','Seaside','Stadium','Station','Traffic','Train'};
classLabels = {'Complain', 'FireAlarm', 'WaterBoiling', 'GlassBreak', 'Doorbell', 'Fall', 'CutleryFall', 'HeavyBreath', 'Rain', 'Help', 'RunningWater', 'Silence'};
classCounter = zeros(length(classLabels), 1);

TESTING_FACTOR = 1; %For extracting all data to one file set this value to one

nSpect_win = spectrogram_win / stStep;
nSpect_step = spectrogram_step / stStep;

D = dir([dirName filesep '*.wav']);
stFeatures = cell(1,length(D));

spectrograms_testing = [];
classIndex_testing = [];

spectrograms_training = [];
classIndex_training = [];

total_spec = 0;
ncmp_spec = nSpect_win * 13;

for i=1:length(D)
    curName = [dirName filesep D(i).name];    
    FileNames{i} = curName;  % get current filename
    index = classindex(curName, classLabels);
    classCounter(index) = classCounter(index) + 1;
end

classCounter_testing = classCounter * TESTING_FACTOR; 

for i = 1:length(classCounter)
    classCounter_testing(i) = floor(classCounter_testing(i)); %Amount of files for testing in each class
end

for i=1:length(D)% for each WAV file
    disp(['Feature extraction for file %50s\n', D(i).name])
    curName = [dirName filesep D(i).name];    
    FileNames{i} = curName;  % get current filename
    % extract short-term features:
    [~ , ~ , stFeaturesPerSegment,stFeat] = ...
        featureExtractionFile(curName, stWin, stStep, 1.25, 0.25, '',{'mfcc'});
    index = classindex(curName, classLabels);
    
    
    classCounter_testing(index) = classCounter_testing(index) - 1;
    
    %First we get the testing data
    if classCounter_testing(index) >= 0
       training = 0;
    else
        training = 1;
    end
    
    nSpect = floor((length(stFeat) / nSpect_step) - nSpect_win/nSpect_step + 1);
    current = 1;
    
    for j=1:nSpect
        spect = stFeat(:, current:(current + nSpect_win - 1));
        spect = reshape(spect, 1, []);
        spect = spect.';
        if training == 1
            spectrograms_training = [spectrograms_training;  transpose(spect)];
            classIndex_training = [classIndex_training; index];
        else
            spectrograms_testing = [spectrograms_testing;  transpose(spect)];
            classIndex_testing = [classIndex_testing; index];           
        end
        
        current = current + nSpect_step;
    end
        
    nspectrograms_training = size(spectrograms_training, 1);
    nClasses_training = size(classIndex_training , 1);
    
    nspectrograms_testing = size(spectrograms_testing, 1);
    nClasses_testing = size(classIndex , 1);
    
end

disp('Extraction Finished');
%% Connect

path_feature_extraction = './Feature extraction';
path_server_functions = './serverFunctions';

addr = '25.120.131.106';
port = 8000;
sensorName = 'kitchen';

sock = serverConnect(addr, port, sensorName);
disp('Connected Successfully!')

%% Send random spectrogram of certain class to Core

classIndex = classIndex_testing;
spectrograms = spectrograms_testing;

prompt = 'Introduce the index of the class [1 to 12]: ';

while 1
    class_count = 0;
    divisor = 20;
    current_2 = 0;
    classLabels
    class = input(prompt);
    while (class > 12 || class < 1)
        disp('Incorrect input reveived')
        class = input(prompt);
    end



    for i=1:size(spectrograms,1)
        if classIndex(i) == class
            class_count = class_count + 1;
        end 
    end

    index = randi([1 class_count]);

    for i=1:size(spectrograms,1)
        if classIndex(i) == class
            index = index - 1;
            if index <= 0
                toSend = spectrograms(i, :);
                break
            end
        end 
    end

    for j = 1:divisor
        serverSendComponents(sock, toSend(:, (current_2 + 1) : current_2 + (nSpect_win * 13/divisor)));
        pause(0.02);
        current_2 = current_2 + (nSpect_win * 13/divisor);
    end

    disp('Components Sent!')
end

    



%% Send Spectograms to separate JSON files (testing + training)



classIndex_testing_aux = classIndex_testing - 1;
classIndex_training_aux = classIndex_training - 1;

if(nClasses_testing > 0)
    disp('Sending testing data to JSON file...')
    output = table(classIndex_testing_aux, spectrograms_testing);
    output_json = jsonencode(output);
    
    %Send to JSON for evaluation of classification parameters in python
    fid = fopen('spectrograms_testing.json','w+');
    fprintf(fid, output_json);
    fclose(fid);
    disp('Done!')
end

if(nClasses_training > 0)
    disp('Sending training data to JSON file...')
    output = table(classIndex_training_aux, spectrograms_training);
    output_json = jsonencode(output);
    
    %Send to JSON for evaluation of classification parameters in python
    fid = fopen('spectrograms_training.json','w+');
    fprintf(fid, output_json);
    fclose(fid);
    disp('Done!')
end



%% Send Spectrograms to JSON file


classIndex = classIndex - 1;


disp('Sending to JSON file...')
output = table(classIndex, spectrograms);
output_json = jsonencode(output);

%Send to JSON for evaluation of classification parameters in python
fid = fopen('spectrograms.json','w+');
fprintf(fid, output_json);
fclose(fid);
disp('Done!')



%% Send to JSON file

for n= 1:length(classIndex_rand)
    classIndex_rand(n) = classIndex_rand(n) - 1;
end

disp('Sending to JSON file...')
components = table(classIndex_rand, features_rand);
components_json = jsonencode(components);

%Send to JSON for evaluation of classification parameters in python
fid = fopen('components.json','w+');
fprintf(fid, components_json);
fclose(fid);
disp('Done!')

%% Send Data
%Connect to python server
sock = serverConnect(addr, port, sensorName);

N_AUDIOS = 10;

for i = 1:N_AUDIOS 
    %Send two audio features (13*2 MFCC components)
    if (serverSendComponents(sock, features_rand(i, :)) == 0) 
        fprintf('Error sending component %d\n',i);
        break;
    end
end

serverDisconnect(sock);
disp('Disconnected from Server')


%% KNN
% Escollim el primer 75% de les dades per entrenar 
learnDB = features_rand(1:round(nExamples*0.75),:);
learnGT = classIndex_rand(1:round(nExamples*0.75),:);
% Escollim el darrer 25% de les dades per testejar 
testDB = features_rand((round(nExamples*0.75)+1):nExamples,:);
testGT = classIndex_rand((round(nExamples*0.75)+1):nExamples,:);

% Generem el model KNN per a classificar amb el conjunt de dades
% d'entrenament
disp('Training KNN ...')
knnModel = fitcknn(learnDB,learnGT,'NumNeighbors',knn_K);
% Avaluem les dades de test amb el model entrenat
disp('Evaluating test data ...')
testCL = predict(knnModel,testDB);



% Comparem les etiquetes reals (testGT) amb les obtingudes amb el
% classificador (testCL)
% --> Accuracy (% de reconeixement global)
% --> F1 (mitja de les mitjanes harm�niques entre precisi� i cobertura de
% cada classe)
okPositions = find(testCL == testGT);
koPositions = find(testCL ~= testGT);
Recall = zeros(nclass,1);
Precision = zeros(nclass,1);
F1 = zeros(nclass,1);
Accuracy = sum(testCL == testGT)/length(testDB);
CM = zeros(nclass); % Confussion matrix
for c = 1:nclass
    TP = length(find(testCL(okPositions) == c));    % True positives = classified as c and correct
    FP = length(find(testCL(koPositions) == c));    % False positives = classified as c and incorrect
    TN = length(find(testCL(okPositions) ~= c));    % True negatives = classified not as c and correct
    FN = length(find(testCL(koPositions) ~= c));    % False negatives = classified not as c and incorrect
    if (TP == 0)
        Rec = 0;Prec = 0;
    else
        Rec = TP/(TP+FN);
        Prec = TP/(TP+FP);
    end
    Recall(c) = Rec;
    Precision(c) = Prec;
    F1(c) = 2/(1/Rec + 1/Prec);

    % Confussion matrix
    cpos = find(testGT == c);
    % Find #examples of class c classified as j
    for j = 1:nclass
        CM(c,j) = CM(c,j) + length(find(testCL(cpos) == j));
    end
end
F1 = sum(F1)/nclass;

disp('   ')
disp(['   F1-macro = ',num2str(F1)]);
disp(['   Accuracy = ',num2str(Accuracy)]);

figure
imagesc(CM);title('Matriu de confusi�');colorbar;


