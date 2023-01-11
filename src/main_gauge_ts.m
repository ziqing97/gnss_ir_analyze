


t1 = posixtime(datetime(2022,10,31,8,30,0,'TimeZone','UTC'));
t2 = posixtime(datetime(2022,10,31,11,30,0,'TimeZone','UTC'));
name = '20221031_gauge.csv';
generate_gauge_ts(t1,t2,name)