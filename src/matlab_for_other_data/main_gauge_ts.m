folder = 'C:/Users/yuziq/Documents/gnss_ir_analyze/data/gauge/';

t1 = posixtime(datetime(2022,8,11,8,30,0,'TimeZone','UTC'));
t2 = posixtime(datetime(2022,8,11,11,30,0,'TimeZone','UTC'));
name = [folder,'20220811_gauge.csv'];
generate_gauge_ts(t1,t2,name)

t1 = posixtime(datetime(2022,9,7,8,30,0,'TimeZone','UTC'));
t2 = posixtime(datetime(2022,9,7,11,30,0,'TimeZone','UTC'));
name = [folder,'20220907_gauge.csv'];
generate_gauge_ts(t1,t2,name)

t1 = posixtime(datetime(2022,10,4,8,30,0,'TimeZone','UTC'));
t2 = posixtime(datetime(2022,10,4,11,30,0,'TimeZone','UTC'));
name = [folder,'20221004_gauge.csv'];
generate_gauge_ts(t1,t2,name)

t1 = posixtime(datetime(2022,10,31,8,30,0,'TimeZone','UTC'));
t2 = posixtime(datetime(2022,10,31,11,30,0,'TimeZone','UTC'));
name = [folder,'20221031_gauge.csv'];
generate_gauge_ts(t1,t2,name)

t1 = posixtime(datetime(2022,11,27,8,30,0,'TimeZone','UTC'));
t2 = posixtime(datetime(2022,11,27,11,30,0,'TimeZone','UTC'));
name = [folder,'20221127_gauge.csv'];
generate_gauge_ts(t1,t2,name)