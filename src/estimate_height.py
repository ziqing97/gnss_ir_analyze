'''
This scipt estimate the height between the
GNSS antenne and the water surface using lomb-
scargle algorithm

Author: Ziqing Yu
Last edited on 14/06/2022
'''
# pylint: disable=invalid-name, bare-except

import os
import random
from datetime import timedelta
import numpy as np
import pandas as pd
# from astropy.timeseries import LombScargle
from scipy import signal
import data_filter as dafi

from pymap3d import enu2geodetic
import gmplot

C = 299792458 # m/s
FREQUENCY_GPS_L1 = 1575.42 * 10**6
WAVELENTH_GPS_S1 = C/FREQUENCY_GPS_L1

FREQUENCY_GLONASS_L1 = 1602 * 10**6
WAVELENTH_GLONASS_S1 = C/FREQUENCY_GLONASS_L1

GOOGLE_APIKEY="AIzaSyBe1VW572pITHH7OBLt1Ziy1e9y0dl4kWw"

def split_result(dataframe,wavelength,time_interval,min_height,max_height):
    '''
    this function does the GNSS-IR analysis for one satellite.
    Args:
        dataframe: dataframe including time, azimut, elevation
                   snr1 and snr2
        time_interval: int, time interval in minutes
        min_height and max_height: the possible heiht range
    Returns:
        time_list: a list of time where a height is estimated
        height_list: the estimated height
        azimut_list: the average azimut
    '''
    time_start = dataframe['time'].iat[0]

    if time_interval>0:
        time_delta = timedelta(minutes=time_interval)
        time_end = time_start + time_delta
    elif time_interval==0:
        time_end=dataframe['time'].iat[-1]
        time_delta=time_end-time_start
    else:
        raise ValueError("time_delta cannot be negativ!")

    time_end = time_start + time_delta
    height_list = []
    time_list = []
    azimut_list = []
    elevation_list = []
    frequency_list =[]
    power_list = []
    while time_end <= dataframe['time'].iat[-1]:
        dataframe_in_interval = dataframe[(dataframe['time'] >= time_start) & \
                                        (dataframe['time'] <= time_end)]
        if not dataframe_in_interval.empty:
            frequency,power,height = estimate_height(dataframe_in_interval,wavelength,min_height,max_height)
            for h in height:
                frequency_list.append(frequency)
                power_list.append(power)
                height_list.append(h)
                time_list.append(time_start + time_delta/2)
                azimut_list.append(np.average(dataframe_in_interval['azimut']))
                elevation_list.append(np.average(dataframe_in_interval['elevation']))
        time_start = time_end
        time_end = time_end = time_start + time_delta
    return (time_list, height_list, azimut_list, elevation_list, frequency_list,power_list)



def estimate_height(dataframe_in_interval, wavelength, min_height, max_height):
    '''
    This function uses LSP to estimate the height:
    Args:
        dataframe_in_interval: dataframe including time, azimut, elevation
                   snr1 and snr2
        min_height and max_height: the possible heiht range
    Returns:
        height: the estimated height during the given time
    '''
    threshold = 2/3
    dataframe_in_interval_sort = dataframe_in_interval.sort_values(by='elevation')
    # sort data by elevation
    elevation_sort = np.array([dataframe_in_interval_sort['elevation']])
    snr = np.array([dataframe_in_interval_sort['snr1']])
    non_nan_index = ~np.isnan(snr)

    # nanfilter
    elevation_filtered = elevation_sort[non_nan_index]
    elevation_filtered = elevation_filtered.reshape(elevation_filtered.size,1)
    snr_filtered = snr[non_nan_index]
    snr_filtered = snr_filtered.reshape(snr_filtered.size,1)

    # calculate the snr_ref
    design_matrix = np.concatenate((elevation_filtered**2,elevation_filtered,\
                np.ones((elevation_filtered.size,1))),axis=1)
    try:
        para = np.dot(np.linalg.solve(np.dot(design_matrix.T,design_matrix),\
                    design_matrix.T),snr_filtered)
    except:
        height = []
        frequency = float("nan")
        power = float("nan")
    else:
        snr_ref = snr_filtered - (elevation_filtered**2 * para[0,0] + \
                    para[1,0]*elevation_filtered + para[2,0])

        # lsp analysis
        x_data = (np.sin(elevation_filtered.T*np.pi/180) * 4 * np.pi / wavelength).ravel()
        y_data = snr_ref.ravel()
        frequency = np.arange(min_height,max_height+1,0.001)

        power = signal.lombscargle(x_data,y_data,frequency,normalize=True)
        peaks,_= signal.find_peaks(power)
        if peaks.size != 0:
            peaks_power = power[peaks]

            height_peak = frequency[peaks]
            height = height_peak[peaks_power>max(peaks_power)*threshold]
        else:
            height = []
    return frequency,power,height

def estimate_all_satellite(main_path:str,azimut_mask:list,elevation_mask:list,min_height:float,max_height:float,time_length:float):
    data_dict = dafi.generate_dataframe(main_path)
    satellite_list = data_dict.keys()
    for satellite_code in satellite_list:
        data_dict[satellite_code] = dafi.azimut_filter(data_dict[satellite_code],azimut_mask)
        data_dict[satellite_code] = dafi.elevation_filter(data_dict[satellite_code],elevation_mask)
    time_dict = {}
    height_dict = {}
    azimut_dict = {}
    elevation_dict ={}
    frequency_dict = {}
    power_dict = {}
    for satellite_code in satellite_list:
        dataframe = data_dict[satellite_code]
        try:
            if satellite_code[0]=='R':
                time_dict[satellite_code], height_dict[satellite_code], azimut_dict[satellite_code],\
                elevation_dict[satellite_code], frequency_dict[satellite_code],power_dict[satellite_code] =\
                split_result(dataframe,WAVELENTH_GLONASS_S1,time_length,min_height=min_height,max_height=max_height)
            else:
                time_dict[satellite_code], height_dict[satellite_code], azimut_dict[satellite_code],\
                elevation_dict[satellite_code], frequency_dict[satellite_code],power_dict[satellite_code] =\
                split_result(dataframe,WAVELENTH_GPS_S1,time_length,min_height=min_height,max_height=max_height)
        except IndexError:
            continue
    return time_dict,height_dict,azimut_dict,elevation_dict,frequency_dict,power_dict

def plot_fresnel_zone(time_str:str, equipment_index:int, azimut_dict:dict, height_dict:dict, elevation_dict:dict) -> None:
    """
    This function will plot the fresnel zone for all valid satellite on map using Google Map API

    Args:
        time_str (str): the date string in form "yyyy-mm-dd"
        equipment_index (int): the equipment or any other index
        azimut_dict (dict): azimut dictionary
        height_dict (dict): height dictionary
        elevation_dict (dict): elevation dictionary
    """    
    file_name = f'{time_str}#{equipment_index}'

    meas_file = os.path.abspath("../data/documentation.xlsx")
    df_meas = pd.read_excel(meas_file)
    lat_center = df_meas[(df_meas["time"]==time_str) & (df_meas["equipment"]==equipment_index)]["latitude"].values[0]
    lon_center = df_meas[(df_meas["time"]==time_str) & (df_meas["equipment"]==equipment_index)]["longitude"].values[0]
    height_center = df_meas[(df_meas["time"]==time_str) & (df_meas["equipment"]==equipment_index)]["height(GNSS)"].values[0]
    sate_name = []
    north_list = []
    east_list = []
    local_height_list = []
    for satellite_code in azimut_dict:
        for i,item in enumerate(azimut_dict[satellite_code]):
            sate_name.append(satellite_code)
            distance = height_dict[satellite_code][i] / np.tan(elevation_dict[satellite_code][0]/180*np.pi)
            azimut = azimut_dict[satellite_code][i]
            
            north_list.append(distance * np.cos(azimut/180*np.pi))
            east_list.append(distance * np.sin(azimut/180*np.pi))
            local_height_list.append(height_dict[satellite_code][i])
    df_coor = pd.DataFrame({"satellite":sate_name,"north":north_list,"east":east_list,"height":local_height_list})

    for index in df_coor.index:
        north = df_coor.loc[index]["north"]
        east = df_coor.loc[index]["east"]
        down = -df_coor.loc[index]["height"]
        (df_coor.loc[index,"lat"],df_coor.loc[index,"lon"],df_coor.loc[index,"alt"])\
            = enu2geodetic(east, north, down, lat_center, lon_center, height_center, ell=None, deg=True)


    gmap = gmplot.GoogleMapPlotter(lat_center,lon_center, 15)
    gmap.scatter([lat_center], [lon_center], '#FF0000', size = 1, marker = True)
    sat_name_plot = "ini"
    for item in df_coor.index:
        lat = df_coor.loc[item]["lat"]
        lon = df_coor.loc[item]["lon"]
        if df_coor.loc[item]["satellite"] != sat_name_plot:
            color = ["#"+"".join([random.choice("0123456789ABCDEF") for j in range(6)])]
            sat_name_plot = df_coor.loc[item]["satellite"]
        gmap.scatter([lat], [lon], color, size = 1, marker = False)
    path = os.path.abspath("../data/color/")
    gmap.draw(f"{path}\\\\{file_name}.html")