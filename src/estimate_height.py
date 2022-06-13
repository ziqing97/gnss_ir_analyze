'''
This scipt estimate the height between the
GNSS antenne and the water surface using lomb-
scargle algorithm
'''
# pylint: disable=invalid-name

from datetime import timedelta
import numpy as np
import matplotlib.pyplot as plt
from astropy.timeseries import LombScargle

WAVELENTH_S1 = 0.1905 # meter

def split_result(dataframe,time_interval,min_height,max_height):
    '''
    function docu
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
    function documents
    '''

    dataframe_in_interval_sort = dataframe_in_interval.sort_values(by='elevation')
    # sort data by elevation
    elevation_sort = np.array([dataframe_in_interval_sort['elevation']])

    # calculate the snr_ref
    design_matrix = np.concatenate((elevation_sort.T**2,elevation_sort.T,\
                    np.ones((np.size(elevation_sort,1),1))),axis=1)
    y = np.array([dataframe_in_interval_sort['snr1']]).T
    x = np.dot(np.linalg.solve(np.dot(design_matrix.T,design_matrix),design_matrix.T),y)
    snr1_ref = y - (elevation_sort.T**2 * x[0,0] + x[1,0]*elevation_sort.T + x[2,0])

    # lsp analysis
    x_data = (np.sin(elevation_sort.T*np.pi/180) * 4 * np.pi / WAVELENTH_S1).ravel()
    y_data = snr1_ref.ravel()
    frequency, power = LombScargle(x_data,y_data).autopower()
    plt.plot(frequency[(frequency < 4)],power[(frequency < 4)])

    # locate the most possible value
    max_power_candidate_idx = (power > max(power)/2)
    height_candidate = frequency[max_power_candidate_idx]
    power_candidate = power[max_power_candidate_idx]

    valid_height_idx = (height_candidate < max_height) & (height_candidate > min_height)
    height_candidate = height_candidate[valid_height_idx]
    power_candidate = power_candidate[valid_height_idx]

    if power_candidate.size != 0:
        max_power_index = (power_candidate == max(power_candidate))
        height = height_candidate[max_power_index]
    else:
        height = float("nan")
    return height
