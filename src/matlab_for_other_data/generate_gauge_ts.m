function[] = generate_gauge_ts(t1,t2,name)
path_to_data = 'C:/Users/yuziq/Documents/RhineStations.nc';
path_to_data = 'C:/Users/yuziq/Documents/gnss_ir_analyze/data/gauge/RhineStations.nc';

data = ncinfo(path_to_data);

t = data.Variables(37).Attributes(5).Value;
surface_elevation = data.Variables(37).Attributes(8).Value;

unix_t = posixtime(datetime(t,'convertfrom','datenum'));

unix_t_extract = unix_t((unix_t>t1) & (unix_t<t2));
s_ele_extract = surface_elevation((unix_t>t1) & (unix_t<t2));

t_extr = datetime(unix_t_extract,'convertfrom','epochtime');

figure
scatter(t_extr,s_ele_extract)

writematrix([[0;unix_t_extract'],[1;s_ele_extract']],name)
end