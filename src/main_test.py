import os
from datetime import datetime,timezone,timedelta
from csv import reader

import numpy as np
import pandas as pd
from astropy.timeseries import LombScargle

import matplotlib.pyplot as plt

from scipy import signal

import data_filter as dafi
import data_process as dapr
import lib_plot
main_path = os.path.abspath('../data/20221031/2/')

azimut_mask = [270,330]
elevation_mask = [0,50]
min_height = 2
max_height = 6
frequency = dapr.generate_frequency(min_height=min_height,max_height=max_height)
starttime = datetime(year=2022,month=10,day=31,hour=8,minute=0,second=0,tzinfo=timezone.utc)
endtime = datetime(year=2022,month=10,day=31,hour=14,minute=0,second=0,tzinfo=timezone.utc)
deltatime = timedelta(minutes=10)

data_dict = dafi.clean_data(main_path,azimut_mask=azimut_mask,elevation_mask=elevation_mask,sn1_trigger=True)


split_data_dict = dafi.split_data(data_dict,starttime,endtime,deltatime)
result_dict,debug_ele,debug_snr = dapr.data_prepare(split_data_dict,frequency=frequency)
print(result_dict)