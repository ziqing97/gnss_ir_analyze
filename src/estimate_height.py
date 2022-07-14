'''
This scipt estimate the height between the
GNSS antenne and the water surface using lomb-
scargle algorithm

Author: Ziqing Yu
Last edited on 14/06/2022
'''
# pylint: disable=invalid-name
# pylint: disable=bare-except

from datetime import timedelta
import numpy as np
import matplotlib.pyplot as plt
# from astropy.timeseries import LombScargle
from scipy import signal

from data_filter import elevation_filter

WAVELENTH_S1 = 0.1905 # meter

def split_result(dataframe,time_interval,min_height,max_height):
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
    time_delta = timedelta(minutes=time_interval)

    time_start = dataframe['time'].iat[0]
    time_end = time_start + time_delta
    height_list = []
    time_list = []
    azimut_list = []
    while time_end < dataframe['time'].iat[-1]:
        dataframe_in_interval = dataframe[(dataframe['time'] >= time_start) & \
                                        (dataframe['time'] < time_end)]
        if not dataframe_in_interval.empty:
            height = estimate_height(dataframe_in_interval,min_height,max_height)
            height_list.append(height)
            time_list.append(time_start + time_delta/2)
            azimut_list.append(np.average(dataframe_in_interval['azimut']))
        time_start = time_end
        time_end = time_end = time_start + time_delta
    return (time_list, height_list, azimut_list)



def estimate_height(dataframe_in_interval, min_height, max_height):
    '''
    This function uses LSP to estimate the height:
    Args:
        dataframe_in_interval: dataframe including time, azimut, elevation
                   snr1 and snr2
        min_height and max_height: the possible heiht range
    Returns:
        height: the estimated height during the given time
    '''

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
        height = float("nan")
    else:
        snr_ref = snr_filtered - (elevation_filtered**2 * para[0,0] + \
                    para[1,0]*elevation_filtered + para[2,0])

        # lsp analysis
        x_data = (np.sin(elevation_filtered.T*np.pi/180) * 4 * np.pi / WAVELENTH_S1).ravel()
        y_data = snr_ref.ravel()
        frequency = np.arange(min_height,max_height+1,0.001)

        power = signal.lombscargle(x_data,y_data,frequency,normalize=True)
        plt.plot(frequency,power)

        peaks,_= signal.find_peaks(power)
        if peaks.size != 0:
            peaks_power = power[peaks]

            height_peak = frequency[peaks]
            height_peak = height_peak[peaks_power==max(peaks_power)]
            height = height_peak
        else:
            height = float("nan")
    return height
