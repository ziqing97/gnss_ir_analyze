from datetime import timedelta
import os

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import transformation
import data_filter as dafi
import estimate_height as esth

main_path = 'E:/OneDrive/Studium/MA/data/20220526/2/'
main_path = os.path.abspath('../data/20220522/2/')

data_dict = dafi.generate_dataframe(main_path)
satellite_list = data_dict.keys()

azimut_mask = [140,320]
elevation_mask = [0,50]
for satellite_code in satellite_list:
    data_dict[satellite_code] = dafi.azimut_filter(data_dict[satellite_code],azimut_mask)
    data_dict[satellite_code] = dafi.elevation_filter(data_dict[satellite_code],elevation_mask)

satellite_code = 'G06'
dataframe = data_dict[satellite_code]
min_height = 1
max_height = 2 # meter
time_interval = 2 # minutes
time_delta = timedelta(minutes=time_interval)

if not dataframe.empty:
    time_list, height_list,azimut_list = esth.split_result(dataframe,time_interval,min_height,max_height)
