%% Init
clc;close all;clearvars

%% Load Data (height in ellipse)
S3Afile = "../../data/altbundle/S3AEsslingen_s1_p3101t586o110sr1000or80.mat";
load(S3Afile)
data = S3AEsslingen_s1_p3101t586o110sr1000or80;

WL_struct = data.ObjTS.Full.WL;
retrack = fields(WL_struct);
retrackname  = {'OCES','OCEP','OGS','ISS','ICES','ICEP','SICS'};

sig_tab = [];
for i=1:length(retrack)
    if i==1
        time = datetime(WL_struct.(retrack{i}).Time,'ConvertFrom','datenum','TimeZone','UTC');
        lat = data.ObjVS.Raw.Sat.Lat.Hi.Ku.Signal;
        lon = data.ObjVS.Raw.Sat.Lon.Hi.Ku.Signal;
        sig_tab = [sig_tab,posixtime(time),lat,lon];
    end
    sig_tab = [sig_tab,WL_struct.(retrack{i}).Signal];
end

tab_title = [{'unixtime'},{'lat'},{'lon'},retrackname];

%% 11.Aug
time_start = datetime(2022,8,11,8,0,0,'TimeZone','UTC');
time_end = datetime(2022,8,11,12,0,0,'TimeZone','UTC');

index = (time>time_start) & (time<time_end);
h_sentinel = sig_tab(index,:);
figure
hold on
for i=1:7
    scatter(datetime(h_sentinel(:,1),'ConvertFrom','epochtime'),h_sentinel(:,i+3))
end
legend(retrackname)
title("11.Aug")
ylabel('meter')

%
T = array2table(h_sentinel, "VariableNames",tab_title);
writetable(T,'../../data/altbundle/20220811sentinel.csv')

%% 07.Sep
time_start = datetime(2022,9,7,8,0,0,'TimeZone','UTC');
time_end = datetime(2022,9,7,12,0,0,'TimeZone','UTC');

index = (time>time_start) & (time<time_end);
h_sentinel = sig_tab(index,:);
figure
hold on
for i=1:7
    scatter(datetime(h_sentinel(:,1),'ConvertFrom','epochtime'),h_sentinel(:,i+3))
end
legend(retrackname)
title("07.Sep")
ylabel('meter')

%
T = array2table(h_sentinel, "VariableNames",tab_title);
writetable(T,'../../data/altbundle/20220907sentinel.csv')

%% 04.Oct
time_start = datetime(2022,10,4,8,0,0,'TimeZone','UTC');
time_end = datetime(2022,10,4,12,0,0,'TimeZone','UTC');

index = (time>time_start) & (time<time_end);
h_sentinel = sig_tab(index,:);
figure
hold on
for i=1:7
    scatter(datetime(h_sentinel(:,1),'ConvertFrom','epochtime'),h_sentinel(:,i+3))
end
legend(retrackname)
title("04.Oct")
ylabel('meter')

%
T = array2table(h_sentinel, "VariableNames",tab_title);
writetable(T,'../../data/altbundle/20221004sentinel.csv')