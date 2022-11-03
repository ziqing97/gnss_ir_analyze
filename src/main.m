clearvars
close all
clc

%%
file20220811_2 = import_fresnel_zone_data("C:\Users\yuziq\Documents\gnss_ir_analyze\src\20220811-2.csv", [2, Inf]);
export20220811_2 = zeros(size(file20220811_2,1),4);
for i = 1:size(file20220811_2,1)
    north = file20220811_2{i,3};
    east = file20220811_2{i,4};
    up = -file20220811_2{i,5};
    lat_center = file20220811_2{i,6};
    lon_center = file20220811_2{i,7};
    height_center = file20220811_2{i,8};
    origin = [lat_center,lon_center,height_center];

    export20220811_2(i,1) = file20220811_2{i,1}; % key
    [export20220811_2(i,2),export20220811_2(i,3),export20220811_2(i,4)] = local2latlon(east,north,up);
end

