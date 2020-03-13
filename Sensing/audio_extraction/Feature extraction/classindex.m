function classIndex = classindex(fileName,classLabels)
% classIndex = classindex(FileNames,classLabels)
% 
% This function returns in classIndex the natural number referred to the
% position of the fileName class in vector classLabels. classLabels is a
% cell array of class labels, and then the fileName belongs to class
% classLabels{classIndex}.

classIndex = [];
for n = 1:length(classLabels)
    k = strfind(fileName,classLabels{n});
    if ~isempty(k)
        classIndex = n;
    end
end
