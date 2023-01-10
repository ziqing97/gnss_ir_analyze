close all;clearvars;clc

path_to_data = 'C:/Users/yuziq/Documents/RhineStations.nc';

data = ncinfo(path_to_data);

t = data.Variables(34).Attributes(5).Value;
surface_elevation = data.Variables(34).Attributes(7).Value;

unix_t = posixtime(datetime(t,'convertfrom','datenum'));

t1 = posixtime(datetime(2022,10,31,8,30,0));
t2 = posixtime(datetime(2022,10,31,11,0,0));

unix_t_extract = unix_t((unix_t>t1) & (unix_t<t2));
s_ele_extract = surface_elevation((unix_t>t1) & (unix_t<t2));

figure
scatter(unix_t_extract,s_ele_extract)
ylim([236,237])

writematrix([[0;unix_t_extract'],[1;s_ele_extract']],'20221031_gauge.csv') 