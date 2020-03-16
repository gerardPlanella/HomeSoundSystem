%% Config 

%Classifier Core IP and port
addr = '127.0.0.1'; %localhost for now
port = 8000;
sensorName = 'kitchen';



% Directori a on tenim les dades etiquetades
dirName = '.\soundscapes';
% Path la carpeta amb les funcions d'extracció de característiques (MFCC)
path_feature_extraction = '.\Feature extraction';

path_server_functions = '.\serverFunctions';



% Simulation parameters
stWin = 100e-3;         % short-term window size (in seconds)
stStep = 50e-3;         % short-term window step (in seconds)
classLabels = {'Bus','Car','CityPark','Classroom','Countryside','Crowd','Factory','Library','Market_pedest','Office','Seaside','Stadium','Station','Traffic','Train'};
knn_K = 3;              % KNN parameter K value
%--------------------------------------------------------------------------
addpath(path_feature_extraction);
addpath(path_server_functions);
% Parametrize dirName WAV files, and obtain feature parameters in
% mtFeatures cell array and filenames in FileNames cell array
disp('Parametritzant corpus ...')
[~, FileNames,stFeatures] =  featureExtractionDir(dirName, stWin, stStep, 0.5, 0.1, '',{'mfcc'});

% Adaptem els atributs d'àudio a les especificacions de la llibreria de ML
% --> features: atributs (N files = trames)x(L = 13 atributs MFCC)
% --> classIndex: classe de cada trama en forma de número enter (N files = trames)x1
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
%% Send Data

% 
% components = table(classIndex_rand, features_rand);
% components_json = jsonencode(components);
% 
% %Send to JSON for evaluation of classification parameters in python
% fid = fopen('components.json','wt');
% fprintf(fid, components_json);
% fclose(fid);
% 
%Connect to python server
sock = serverConnect(addr, port, sensorName);

N_AUDIOS = 2;

for i = 1:N_AUDIOS 
    %Send two audio features (13*2 MFCC components)
    if (serverSendComponents(sock, features_rand(i, :)) == 0) 
        fprintf('Error sending component %d\n',i);
        break;
    end
end

serverDisconnect(sock);
disp('Disconnected from Server')


%% KNN: Done in python [Miquel & Gerard]
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
% --> F1 (mitja de les mitjanes harmòniques entre precisió i cobertura de
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
imagesc(CM);title('Matriu de confusió');colorbar;


