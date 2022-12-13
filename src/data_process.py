"""
This script does the calculation of the gnss-ir
analyse

"""
from scipy import signal
import numpy as np

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
            wavelength = WAVELENTH_GLONASS_S1
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

def extract_height_as_max_peak(result_dict,frequency):
    """
    this function extracts the height from the maximal height
    Args:
        result_dict (_type_): _description_
        frequency (_type_): _description_

    Returns:
        _type_: _description_
    """
    result_dict_copy = result_dict
    for satellite_code in result_dict_copy:
        result_dict_copy[satellite_code]['maximal_height'] = []
        for power in result_dict_copy[satellite_code]['power']:
            peaks,_= signal.find_peaks(power)
            if peaks.size != 0:
                power_at_peak = power[peaks]
                height_at_peak = frequency[peaks]
                height = height_at_peak[power_at_peak==max(power_at_peak)]
                result_dict_copy[satellite_code]['maximal_height'].append(height[0])
            else:
                result_dict_copy[satellite_code]['maximal_height'].append(float('nan'))
    return result_dict_copy
