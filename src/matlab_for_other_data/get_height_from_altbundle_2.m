%% Init
clc;close all;clearvars

%% Load Data (height in ellipse)
S3Afile = "../../data/altbundle/S3AEsslingen_s1_p3101t586o110sr800or80.mat";
load(S3Afile)
data = S3AEsslingen_s1_p3101t586o110sr800or80;

WL_struct = data.ObjTS.DownSampled.WL;
retrack = fields(WL_struct);
retrackname  = {'OCES','OCEP','OGS','ISS','ICES','ICEP','SICS'};
retrackucname  = {'OCESuc','OCEPuc','OGSuc','ISSuc','ICESuc','ICEPuc','SICSuc'};
table_head = [{'unixtime'}, retrackname,retrackucname];

sig_tab = [];
time_list = [];
for i=1:length(retrack)
    if i==1
        time = datetime(WL_struct.(retrack{i}).Mean.Time,'ConvertFrom','datenum','TimeZone','UTC');
%         lat = data.ObjVS.Raw.Sat.Lat.Hi.Ku.Signal;
%         lon = data.ObjVS.Raw.Sat.Lon.Hi.Ku.Signal;
        sig_tab = [sig_tab,posixtime(time)];
    end
    sig_tab = [sig_tab,WL_struct.(retrack{i}).Mean.Signal];
    time_list = [time_list, time];
end

for i=1:length(retrack)
    sig_tab = [sig_tab,WL_struct.(retrack{i}).Mean.Error];
end

% 11.Aug
time_start = datetime(2022,8,11,8,0,0,'TimeZone','UTC');
time_end = datetime(2022,8,11,12,0,0,'TimeZone','UTC');

index = (time>time_start) & (time<time_end);
h_sentinel = sig_tab(index,:);
figure
hold on
for i=1:7
    scatter(h_sentinel(:,1),h_sentinel(:,i+3))
end
title("11.Aug")
ylabel('meter')
legend(retrackname)
T = array2table(h_sentinel,'VariableNames',table_head);
writetable(T,'../../data/altbundle/20220811sentinel2.csv')

% 07.Sep
time_start = datetime(2022,9,7,8,0,0,'TimeZone','UTC');
time_end = datetime(2022,9,7,12,0,0,'TimeZone','UTC');

index = (time>time_start) & (time<time_end);
h_sentinel = sig_tab(index,:);
figure
hold on
for i=1:7
    scatter(h_sentinel(:,1),h_sentinel(:,i+3))
end
title("07.Sep")
ylabel('meter')
legend(retrackname)
T = array2table(h_sentinel,'VariableNames',table_head);
writetable(T,'../../data/altbundle/20220907sentinel2.csv')

% 04.Oct
time_start = datetime(2022,10,4,8,0,0,'TimeZone','UTC');
time_end = datetime(2022,10,4,12,0,0,'TimeZone','UTC');

index = (time>time_start) & (time<time_end);
h_sentinel = sig_tab(index,:);
figure
hold on
for i=1:7
    scatter(h_sentinel(:,1),h_sentinel(:,i+3))
end
title("04.Oct")
ylabel('meter')
legend(retrackname)
T = array2table(h_sentinel,'VariableNames',table_head);
writetable(T,'../../data/altbundle/20221004sentinel2.csv')

% 31.Oct
time_start = datetime(2022,10,31,8,0,0,'TimeZone','UTC');
time_end = datetime(2022,10,31,12,0,0,'TimeZone','UTC');

index = (time>time_start) & (time<time_end);
h_sentinel = sig_tab(index,:);
figure
hold on
for i=1:7
    scatter(h_sentinel(:,1),h_sentinel(:,i+3))
end
title("31.Oct")
ylabel('meter')
legend(retrackname)
T = array2table(h_sentinel,'VariableNames',table_head);
writetable(T,'../../data/altbundle/20221031sentinel2.csv')

% 27.Nov
time_start = datetime(2022,11,27,8,0,0,'TimeZone','UTC');
time_end = datetime(2022,11,27,12,0,0,'TimeZone','UTC');

index = (time>time_start) & (time<time_end);
h_sentinel = sig_tab(index,:);
figure
hold on
for i=1:7
    scatter(h_sentinel(:,1),h_sentinel(:,i+3))
end
title("27.Nov")
ylabel('meter')
legend(retrackname)
T = array2table(h_sentinel,'VariableNames',table_head);
writetable(T,'../../data/altbundle/20221127sentinel2.csv')


% 16.February
time_start = datetime(2023,2,16,7,0,0,'TimeZone','UTC');
time_end = datetime(2023,2,16,18,0,0,'TimeZone','UTC');

index = (time>time_start) & (time<time_end);
h_sentinel = sig_tab(index,:);
figure
hold on
for i=1:7
    scatter(h_sentinel(:,1),h_sentinel(:,i+3))
end
title("16.February")
ylabel('meter')
legend(retrackname)
T = array2table(h_sentinel,'VariableNames',table_head);
writetable(T,'../../data/altbundle/20230216sentinel2.csv')

% 15.March
time_start = datetime(2023,3,15,7,0,0,'TimeZone','UTC');
time_end = datetime(2023,3,15,18,0,0,'TimeZone','UTC');

index = (time>time_start) & (time<time_end);
h_sentinel = sig_tab(index,:);
figure
hold on
for i=1:7
    scatter(h_sentinel(:,1),h_sentinel(:,i+3))
end
title("15.March")
ylabel('meter')
legend(retrackname)
T = array2table(h_sentinel,'VariableNames',table_head);
writetable(T,'../../data/altbundle/20230315sentinel2.csv')