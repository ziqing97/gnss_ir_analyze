%% Init
clc;close all;clearvars

%% Load Data (height in ellipse)
S3Afile = "../../data/altbundle/S3AEsslingen_s1_p3101t586o110sr800or80.mat";
load(S3Afile)
data = S3AEsslingen_s1_p3101t586o110sr800or80;

WL_struct = data.ObjTS.Full.WL;
retrack = fields(WL_struct);
retrackname  = {'OCES','OCEP','OGS','ISS','ICES','ICEP','SICS'};

sig_tab = [];
for i=1:length(retrack)
    if i==1
        time = datetime(WL_struct.(retrack{i}).Time,'ConvertFrom','datenum','TimeZone','UTC');
        sig_tab = [sig_tab,posixtime(time)/1000];
    end
    sig_tab = [sig_tab,WL_struct.(retrack{i}).Signal];
end

% 11.Aug
time_start = datetime(2022,8,11,8,0,0,'TimeZone','UTC');
time_end = datetime(2022,8,11,12,0,0,'TimeZone','UTC');

index = (time>time_start) & (time<time_end);
h_sentinel = sig_tab(index,:);
figure
hold on
for i=1:7
    scatter(h_sentinel(:,1),h_sentinel(:,i+1))
end
title("11.Aug")
ylabel('meter')

% 07.Sep
time_start = datetime(2022,9,7,8,0,0,'TimeZone','UTC');
time_end = datetime(2022,9,7,12,0,0,'TimeZone','UTC');

index = (time>time_start) & (time<time_end);
h_sentinel = sig_tab(index,:);
figure
hold on
for i=1:7
    scatter(h_sentinel(:,1),h_sentinel(:,i+1))
end
title("07.Sep")
ylabel('meter')

% 04.Oct
time_start = datetime(2022,10,4,8,0,0,'TimeZone','UTC');
time_end = datetime(2022,10,4,12,0,0,'TimeZone','UTC');

index = (time>time_start) & (time<time_end);
h_sentinel = sig_tab(index,:);
figure
hold on
for i=1:7
    scatter(h_sentinel(:,1),h_sentinel(:,i+1))
end
title("04.Oct")
ylabel('meter')

% 31.Oct
time_start = datetime(2022,10,31,8,0,0,'TimeZone','UTC');
time_end = datetime(2022,10,31,12,0,0,'TimeZone','UTC');

index = (time>time_start) & (time<time_end);
h_sentinel = sig_tab(index,:);
figure
hold on
for i=1:7
    scatter(h_sentinel(:,1),h_sentinel(:,i+1))
end
title("31.Oct")
ylabel('meter')

% 27.Nov
time_start = datetime(2022,11,27,8,0,0,'TimeZone','UTC');
time_end = datetime(2022,11,27,12,0,0,'TimeZone','UTC');

index = (time>time_start) & (time<time_end);
h_sentinel = sig_tab(index,:);
figure
hold on
for i=1:7
    scatter(h_sentinel(:,1),h_sentinel(:,i+1))
end
title("27.Nov")
ylabel('meter')