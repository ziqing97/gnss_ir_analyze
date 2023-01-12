clc

S3Afile = "C:\Users\yuziq\Documents\gnss_ir_analyze\data\S3AEsslingen_s1_p3101t586o110sr1000or80.mat";
load(S3Afile)

lat = S3AEsslingen_s1_p3101t586o110sr1000or80.ObjVS.Gen.Sat.Lat.Hi.C.Signal;
lon = S3AEsslingen_s1_p3101t586o110sr1000or80.ObjVS.Gen.Sat.Lon.Hi.C.Signal;
time = S3AEsslingen_s1_p3101t586o110sr1000or80.ObjVS.Gen.Sat.Lon.Hi.C.Time;
time = datetime(time,'ConvertFrom','datenum');

lat = S3AEsslingen_s1_p3101t586o110sr1000or80.ObjVS.Raw.Sat.Lat.Hi.C.Signal;
lon = S3AEsslingen_s1_p3101t586o110sr1000or80.ObjVS.Raw.Sat.Lon.Hi.C.Signal;
time = S3AEsslingen_s1_p3101t586o110sr1000or80.ObjVS.Raw.Sat.Lon.Hi.C.Time;
time = datetime(time,'ConvertFrom','datenum');

% 导出
% unix_t = posixtime(datetime(t,'convertfrom','datenum'));
% result
% writematrix