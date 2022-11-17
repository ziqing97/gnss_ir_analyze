'''
This scipt estimate the height between the
GNSS antenne and the water surface using lomb-
scargle algorithm

Author: Ziqing Yu
Last edited on 14/06/2022
'''
# pylint: disable=invalid-name, bare-except

import os
from datetime import timedelta
from csv import reader

import numpy as np
import pandas as pd
# from astropy.timeseries import LombScargle
from scipy import signal

from pymap3d import enu2geodetic
import gmplot

import data_filter as dafi

C = 299792458 # m/s
FREQUENCY_GPS_L1 = 1575.42 * 10**6
WAVELENTH_GPS_S1 = C/FREQUENCY_GPS_L1

FREQUENCY_GLONASS_L1 = 1602 * 10**6
WAVELENTH_GLONASS_S1 = C/FREQUENCY_GLONASS_L1

GOOGLE_APIKEY="AIzaSyBe1VW572pITHH7OBLt1Ziy1e9y0dl4kWw"
def get_satellite_color() -> dict:
    """
    read satellite color from the file
    Returns:
        dict: a dict with satellite code as key and color as value
    """
    color_file = os.path.abspath('../data/color/gnss_color.csv')
    color_dict = {}
    with open(color_file, 'r', encoding='utf8') as read_obj:
        csv_reader = reader(read_obj)
        for row in csv_reader:
            color_dict[row[0]]=row[1]
    del color_dict['']
    return color_dict

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
            frequency,power,height =\
                estimate_height(dataframe_in_interval,wavelength,min_height,max_height)
            for h in height:
                frequency_list.append(frequency)
                power_list.append(power)
                height_list.append(h)
                time_list.append(time_start + time_delta/2)
                azi_info = {'avg':np.average(dataframe_in_interval['azimut']),\
                            'max':max(dataframe_in_interval['azimut']),\
                            'min':min(dataframe_in_interval['azimut'])}
                azimut_list.append(azi_info)
                ele_info = {'avg':np.average(dataframe_in_interval['elevation']),\
                            'max':max(dataframe_in_interval['elevation']),\
                            'min':min(dataframe_in_interval['elevation'])}
                elevation_list.append(ele_info)
        time_start = time_end
        time_end = time_end = time_start + time_delta
    return (time_list, height_list, azimut_list, elevation_list, frequency_list,power_list)

def estimate_height(dataframe_in_interval:pd.DataFrame, wavelength, min_height, max_height):
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

def estimate_all_satellite(main_path:str,azimut_mask:list,elevation_mask:list,\
    min_height:float,max_height:float,time_length:float):
    """
    Esmite all satellite results
    Args:
        main_path (str): _description_
        azimut_mask (list): _description_
        elevation_mask (list): _description_
        min_height (float): _description_
        max_height (float): _description_
        time_length (float): _description_

    Returns:
        _type_: _description_
    """
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
                time_dict[satellite_code], height_dict[satellite_code],\
                    azimut_dict[satellite_code],\
                elevation_dict[satellite_code], frequency_dict[satellite_code],\
                    power_dict[satellite_code] =\
                split_result(dataframe,WAVELENTH_GLONASS_S1,time_length,\
                    min_height=min_height,max_height=max_height)
            else:
                time_dict[satellite_code], height_dict[satellite_code],\
                    azimut_dict[satellite_code],\
                elevation_dict[satellite_code], frequency_dict[satellite_code],\
                    power_dict[satellite_code] =\
                split_result(dataframe,WAVELENTH_GPS_S1,time_length,\
                    min_height=min_height,max_height=max_height)
        except IndexError:
            continue
    return time_dict,height_dict,azimut_dict,elevation_dict,frequency_dict,power_dict

def __calc_fresnel_zone(wave_length:float,height:float,elevation:float,azimut:float):
    elevation = elevation/180*np.pi
    azimut = azimut/180*np.pi

    d = wave_length/2
    r = height / np.tan(elevation)+(d/np.sin(elevation)) / np.tan(elevation)
    b = np.sqrt(2*d*height/np.sin(elevation) + np.square(d/np.sin(elevation)))
    a = b/np.sin(elevation)

    theta = np.linspace(0,2*np.pi,num=200)
    x_new = a * np.cos(theta) + r
    y_new = b * np.sin(theta)

    east = np.sin(azimut)*x_new - np.cos(azimut)*y_new
    north = np.sin(azimut)*y_new + np.cos(azimut)*x_new
    return east,north

def plot_fresnel_zone(time_str:str, equipment_index:int,\
    azimut_dict:dict, height_dict:dict, elevation_dict:dict) -> None:
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
    lat_center = df_meas[(df_meas["time"]==time_str) &\
        (df_meas["equipment"]==equipment_index)]["latitude"].values[0]
    lon_center = df_meas[(df_meas["time"]==time_str) &\
        (df_meas["equipment"]==equipment_index)]["longitude"].values[0]
    height_center = df_meas[(df_meas["time"]==time_str) &\
        (df_meas["equipment"]==equipment_index)]["height(GNSS)"].values[0]
    sate_name = []
    north_list = []
    east_list = []
    local_height_list = []
    for satellite_code in azimut_dict:
        if satellite_code[0]=='R':
            wave_length = WAVELENTH_GLONASS_S1
        else:
            wave_length = WAVELENTH_GPS_S1
        for i,_ in enumerate(azimut_dict[satellite_code]):
            azimut = azimut_dict[satellite_code][i]
            elevation = elevation_dict[satellite_code][i]
            height = height_dict[satellite_code][i]
            east,north = __calc_fresnel_zone(wave_length,height,elevation,azimut)

            sate_name.append(satellite_code)
            north_list.append(north)
            east_list.append(east)
            local_height_list.append(height_dict[satellite_code][i])

    color_dict = get_satellite_color()
    gmap = gmplot.GoogleMapPlotter(lat_center,lon_center, 15)
    gmap.scatter([lat_center], [lon_center], '#FF0000', size = 1, marker = True)
    sat_name_plot = "ini"
    for i,sate in enumerate(sate_name):
        north = north_list[i]
        east = east_list[i]
        down = -east_list[i]
        (lat,lon,_) = enu2geodetic(east, north, down, lat_center,\
            lon_center, height_center, deg=True)

        if sate != sat_name_plot:
            color = color_dict[sate]
            sat_name_plot = sate
        gmap.plot(lats=lat, lngs=lon, color=color, edge_width=1)
    path = os.path.abspath("../data/fresnel_zone/")
    gmap.draw(f"{path}\\\\{file_name}.html")
