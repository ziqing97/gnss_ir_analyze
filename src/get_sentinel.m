clc

S3Afile = "../../S3A/S3A1004_p3101t586o110sr2000wo1or99.mat";
load(S3Afile)

lat = S3A1004_p3101t586o110sr2000wo1or99.ObjVS.Gen.Sat.Lat.Hi.C.Signal;
lon = S3A1004_p3101t586o110sr2000wo1or99.ObjVS.Gen.Sat.Lon.Hi.C.Signal;
time = S3A1004_p3101t586o110sr2000wo1or99.ObjVS.Gen.Sat.Lon.Hi.C.Time;
time = datetime(time,'ConvertFrom','datenum');

lat = S3A1004_p3101t586o110sr2000wo1or99.ObjVS.Raw.Sat.Lat.Hi.C.Signal;
lon = S3A1004_p3101t586o110sr2000wo1or99.ObjVS.Raw.Sat.Lon.Hi.C.Signal;
time = S3A1004_p3101t586o110sr2000wo1or99.ObjVS.Raw.Sat.Lon.Hi.C.Time;
time = datetime(time,'ConvertFrom','datenum');