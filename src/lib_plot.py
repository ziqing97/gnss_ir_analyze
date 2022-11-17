'''
This script provides the function for plotting

Author: Ziqing Yu
Last edited on 14/06/2022
'''

import os
from csv import reader

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import matplotlib.cm as cm

import gmplot
from pymap3d import enu2geodetic

C = 299792458 # m/s
FREQUENCY_GPS_L1 = 1575.42 * 10**6
WAVELENTH_GPS_S1 = C/FREQUENCY_GPS_L1

FREQUENCY_GLONASS_L1 = 1602 * 10**6
WAVELENTH_GLONASS_S1 = C/FREQUENCY_GLONASS_L1

GOOGLE_APIKEY="AIzaSyBe1VW572pITHH7OBLt1Ziy1e9y0dl4kWw"
# pylint:disable=invalid-name

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

def plot_ele_azi_height(title,elevation_dict:dict,azimut_dict:dict,height_dict:dict) -> None:
    """
    This function plot the height where elevation as the x-axis,
    azimut as the y-axis and height as a colorbar

    Args:
        elevation_dict (dict): _description_
        azimut_dict (dict): _description_
        height_dict (dict): _description_
    """
    ele_plot=[]
    ele_err = [[],[]]
    azi_plot=[]
    azi_err=[[],[]]
    h_plot=[]
    for satellite_code in elevation_dict:
        for i,_ in enumerate(elevation_dict[satellite_code]):
            for h in height_dict[satellite_code]:
                ele_plot.append(elevation_dict[satellite_code][i]['avg'])
                ele_err[0].append(elevation_dict[satellite_code][i]['avg']-\
                elevation_dict[satellite_code][i]['min'])
                ele_err[1].append(elevation_dict[satellite_code][i]['max']-\
                    elevation_dict[satellite_code][i]['avg'])
                azi_plot.append(azimut_dict[satellite_code][i]['avg'])
                azi_err[0].append(azimut_dict[satellite_code][i]['avg']-\
                    azimut_dict[satellite_code][i]['min'])
                azi_err[1].append(azimut_dict[satellite_code][i]['max']-\
                    azimut_dict[satellite_code][i]['avg'])
                h_plot.append(h)

    norm = plt.Normalize(vmin=min(h_plot),vmax=max(h_plot))
    norm = matplotlib.colors.Normalize(vmin=min(h_plot),vmax=max(h_plot), clip=True)
    mapper = cm.ScalarMappable(norm=norm, cmap='jet')
    h_color = np.array([(mapper.to_rgba(v)) for v in h_plot])
    fig=plt.scatter(ele_plot,azi_plot,c=h_plot,cmap='jet')# RdBu,coolwarm,hsv tried
    plt.colorbar(fig)
    for ele, azi, e_min, e_max, a_min, a_max, color in zip(ele_plot, azi_plot,\
        ele_err[0],ele_err[1], azi_err[0], azi_err[1], h_color):
        e_range = np.array([e_min,e_max]).reshape(2,1)
        a_range = np.array([a_min,a_max]).reshape(2,1)
        plt.errorbar(ele, azi, xerr=e_range, yerr=a_range, lw=1, capsize=3, color=color)
    plt.title(title)
    plt.xlabel("elevation")
    plt.ylabel("azimut")
