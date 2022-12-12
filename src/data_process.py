"""
This script does the calculation of the gnss-ir
analyse

"""
from scipy import signal
import numpy as np

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

    power = signal.lombscargle(x_data,y_data,frequency,normalize=True)
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
