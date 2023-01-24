%% Init
clc;close all;clearvars

%% Load Data (height in ellipse)
S3Afile = "C:\Users\yuziq\Documents\gnss_ir_analyze\data\altbundle\S3AEsslingen_s1_p3101t586o110sr1000or80.mat";
load(S3Afile)
data = S3AEsslingen_s1_p3101t586o110sr1000or80;



%% get the height timeseries
[t1,h1] = extract_height_from_altbundle(data);

%% extract the data from valid time
% 07.Sep
figure
subplot(2,1,1)
time_start = datetime(2022,9,7,8,0,0,'TimeZone','UTC');
time_end = datetime(2022,9,7,12,0,0,'TimeZone','UTC');

index = (t1>time_start) & (t1<time_end);
t_valid = t1(index);
h_valid = h1(index);
scatter(t_valid,h_valid)
title("07.Sep")
ylabel('meter')


% 04.Oct
subplot(2,1,2)
time_start = datetime(2022,10,04,8,0,0,'TimeZone','UTC');
time_end = datetime(2022,10,04,12,0,0,'TimeZone','UTC');

index = (t1>time_start) & (t1<time_end);
t_valid = t1(index);
h_valid = h1(index);
scatter(t_valid,h_valid)
title("04.Oct")
ylabel('meter')