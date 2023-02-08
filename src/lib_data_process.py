"""
This script does the calculation of the gnss-ir
analyse

"""
from datetime import datetime,timedelta,timezone

from scipy import signal
import numpy as np
from tqdm import tqdm


import data_filter as dafi

# pylint:disable=invalid-name,consider-using-dict-items

C = 299792458 # m/s
FREQUENCY_GPS_L1 = 1575.42 * 10**6
WAVELENTH_GPS_S1 = C/FREQUENCY_GPS_L1

FREQUENCY_GLONASS_L1 = 1602 * 10**6
WAVELENTH_GLONASS_S1 = C/FREQUENCY_GLONASS_L1

def calc_lsp_power(elevation_sort,snr_sort,frequency,wavelength):
    """
    this function calculates the lsp power

    Args:
        elevation_sort (np.array): _description_
        snr_sort (np.array): _description_
        frequency (np.array): _description_
        wavelength (float): _description_

    Returns:
        _type_: _description_
    """
    design_matrix = np.concatenate((elevation_sort**2,elevation_sort,\
                np.ones((elevation_sort.size,1))),axis=1)
    para = np.dot(np.linalg.solve(np.dot(design_matrix.T,design_matrix),\
                    design_matrix.T),snr_sort)
    snr_ref = snr_sort - (elevation_sort**2 * para[0,0] + \
                    para[1,0]*elevation_sort + para[2,0])
    x_data = (np.sin(elevation_sort.T*np.pi/180) * 4 * np.pi / wavelength).ravel()
    y_data = snr_ref.ravel()
    try:
        power = signal.lombscargle(x_data,y_data,frequency,normalize=True)
    except AssertionError:
        power = frequency
    return power

def extract_azimut(azimut_array):
    """
    extract the azimut information of the data
    Args:
        azimut_array: the azimut array

    Returns:
        a dict of the azimut info
    """
    temp = {}
    temp['avg'] = np.average(azimut_array)
    temp['min'] = min(azimut_array)
    temp['max'] = max(azimut_array)
    return temp

def extract_elevation(elevation_array):
    """
    extract the elevation information of the data
    Args:
        elevation_array: the elevation array

    Returns:
        a dict of the elevation info
    """
    temp = {}
    temp['avg'] = np.average(elevation_array)
    temp['min'] = min(elevation_array)
    temp['max'] = max(elevation_array)
    return temp

def generate_frequency(min_height,max_height):
    """
    generate the frequency basis for lsp
    Args:
        min_height (_type_): minimum height
        max_height (_type_): maximum height

    Returns:
        _type_: frequency for lsp in np array
    """
    frequency = np.arange(min_height,max_height,0.001)
    return frequency

def data_prepare(split_data_dict,frequency):
    """
    this function does all the necessary things

    Args:
        split_data_dict (_type_): _description_
        min_height (_type_): _description_
        max_height (_type_): _description_

    Returns:
        _type_: _description_
    """
    split_data_dict_copy = split_data_dict

    for satellite_code in split_data_dict_copy:
        # get the right wavelength
        if satellite_code[0]=='R':
            frequency_base = FREQUENCY_GLONASS_L1
            channel = int(satellite_code[1:])
            frequency_glo = frequency_base + channel * 0.5625 * 10**6
            wavelength = C / frequency_glo
        else:
            wavelength = WAVELENTH_GPS_S1

        # init the list for power
        split_data_dict_copy[satellite_code]['power'] = []
        split_data_dict_copy[satellite_code]['elevation'] = []
        split_data_dict_copy[satellite_code]['azimut'] = []

        # a loop to calculate the power
        for item in split_data_dict_copy[satellite_code]['raw']:
            # sort data by elevation
            dataframe_sort = item.sort_values(by='elevation')

            # get the elevation and azimut information
            ele_dict = extract_azimut(dataframe_sort.loc[:]['elevation'])
            azi_dict = extract_azimut(dataframe_sort.loc[:]['azimut'])
            split_data_dict_copy[satellite_code]['elevation'].append(ele_dict)
            split_data_dict_copy[satellite_code]['azimut'].append(azi_dict)

            # do the lsp analyse
            elevation_sort = np.array([dataframe_sort['elevation']]).T
            snr_sort = np.array([dataframe_sort['snr1']]).T
            power = calc_lsp_power(elevation_sort,snr_sort,frequency,wavelength)
            split_data_dict_copy[satellite_code]['power'].append(power)

            # get the possible height
    return split_data_dict_copy

def generate_power_likelihood(result_dict):
    """
    this function generates the power likelihood
    using all lsp
    Args:
        result_dict (_type_): _description_

    Returns:
        _type_: _description_
    """
    power_likelyhood = 1
    for satellite_code in result_dict:
        for sig in result_dict[satellite_code]['power']:
            power_likelyhood = np.multiply(sig,power_likelyhood)
    return power_likelyhood

def scale_power_to_unit_area(x,y):
    """
    calculate the area of a function to unit area
    Args:
        x (_type_): _description_
        y (_type_): _description_

    Returns:
        _type_: _description_
    """
    area = np.sum(np.multiply((x[2:]-x[0:-2])/2, y[1:-1]))
    scale = 1/area
    y_scaled = y*scale
    return y_scaled

def generate_timeseries(main_path, azimut_mask, elevation_mask, \
    min_height, max_height, t_range, month, day):
    """

    Args:
        main_path (_type_): _description_
        azimut_mask (_type_): _description_
        elevation_mask (_type_): _description_
        min_height (_type_): _description_
        max_height (_type_): _description_
        t_range (_type_): _description_

    Returns:
        _type_: _description_
    """
    frequency = generate_frequency(min_height=min_height,max_height=max_height)
    signal_ts = {}

    for dt in tqdm(range(0,t_range-1)):
        starttime = datetime(year=2022,month=month,day=day,hour=8,\
            minute=0+dt,second=0,tzinfo=timezone.utc)
        endtime = datetime(year=2022,month=month,day=day,hour=14,\
            minute=0+dt,second=0,tzinfo=timezone.utc)
        deltatime = timedelta(minutes=t_range)

        data_dict = dafi.clean_data(main_path,azimut_mask=azimut_mask,\
            elevation_mask=elevation_mask,sn1_trigger=True)

        split_data_dict = dafi.split_data(data_dict,starttime,endtime,deltatime)
        result_dict = data_prepare(split_data_dict,frequency=frequency)

        for satellite_code in result_dict:
            for t,p in zip(result_dict[satellite_code]['time'],\
                result_dict[satellite_code]['power']):
                if t in signal_ts:
                    signal_ts[t] = np.multiply(p,signal_ts[t])
                else:
                    signal_ts[t] = p
    height_ts = {}
    for t in signal_ts:
        p = signal_ts[t]

        index_peak, _ = signal.find_peaks(p)
        if index_peak.size != 0:
            p_inpeak = p[index_peak]
            f_inpeak = frequency[index_peak]
            index_max = p_inpeak==max(p_inpeak)
            h = f_inpeak[index_max]
            height_ts[t] = h[0]
        else:
            height_ts[t] = np.nan
    return height_ts
