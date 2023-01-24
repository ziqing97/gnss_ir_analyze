%% Init
clc;close all;clearvars

%% Load Data (height in ellipse)
S3Afile = "C:\Users\yuziq\Documents\gnss_ir_analyze\data\altbundle\S3AEsslingen_s1_p3101t586o110sr1000or80.mat";
load(S3Afile)
data = S3AEsslingen_s1_p3101t586o110sr1000or80;

WL_struct = data.ObjTS.Full.WL;
retrack = fields(WL_struct);

figure
hold on
for i=1:length(retrack)
    time = datetime(WL_struct.(retrack{i}).Time,'ConvertFrom','datenum');
    sign = WL_struct.(retrack{i}).Signal;
    cycl = WL_struct.(retrack{i}).Cycle;
    scatter(time,sign)
end
legend(retrack)