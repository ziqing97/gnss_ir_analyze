'''
This script generates for each satellite a pands
dataframe and filters the data so that they are in
a right elevation and azimut range
'''

import pandas as pd
import read_compact_data as rcd


def generate_dataframe(main_path):
    '''
    this function generates a dictionary of pandas
    dataframes where for each satellite the necessary
    data are stored
    Args:
        main_path: where all compactfiles exist
    Returns:
        a dict of pandas dataframe where the keys
        are the the satellite names and values are
        a dataframe with elevation, azimut, snr1,
        snr2
    '''
    data_dict = rcd.generate_database(main_path)

    azi_data = data_dict['azi']
    ele_data = data_dict['ele']
    sn1_data = data_dict['sn1']
    sn2_data = data_dict['sn2']

    satellite_list = data_dict['ele'].keys()

    dataframe_dict = {}
    for satellite_code in satellite_list:
        df_azimut = pd.DataFrame({'time':azi_data[satellite_code]['time'],\
            'azimut':azi_data[satellite_code]['azi']})
        df_elevation = pd.DataFrame({'time':ele_data[satellite_code]['time'],\
            'elevation':ele_data[satellite_code]['ele']})
        if satellite_code in sn1_data:
            df_snr1 = pd.DataFrame({'time':sn1_data[satellite_code]['time'],\
                'snr1':sn1_data[satellite_code]['sn1']})
        else:
            df_snr1 = pd.DataFrame({'time':[],'snr1':[]})
        if satellite_code in sn2_data:
            df_snr2 = pd.DataFrame({'time':sn2_data[satellite_code]['time'],\
                'snr2':sn2_data[satellite_code]['sn2']})
        else:
            df_snr2 = pd.DataFrame({'time':[],'snr1':[]})

        dataframe = pd.merge(df_azimut,df_elevation,on=['time'],how='inner')
        dataframe = pd.merge(dataframe,df_snr1,on=['time'],how='inner')
        dataframe = pd.merge(dataframe,df_snr2,on=['time'],how='inner')
        dataframe_dict[satellite_code] = dataframe
    return dataframe_dict

def azimut_filter(dataframe,azimut_mask):
    '''
    this function filter the data using an azimut
    mask
    Args:
        dataframe: dataframe generated from 'generate dataframe'
        azimut_mask: a list with 2 elements [min, max] in clockwise
                     direction
    Returns:
        dataframe after azimut filtering
    '''
    if azimut_mask[0] < azimut_mask[1]:
        azimut_index = (dataframe['azimut'] > azimut_mask[0]) & \
            (dataframe['azimut'] < azimut_mask[1])
    else:
        azimut_index = (dataframe['azimut'] > azimut_mask[0]) | \
            (dataframe['azimut'] < azimut_mask[1])
    dataframe = dataframe[azimut_index]
    return dataframe

def elevation_filter(dataframe,elevation_mask):
    '''
    this function filter the data using an elevation
    mask
    Args:
        dataframe: dataframe generated from 'generate dataframe'
        elevation_mask: a list with 2 elements [min, max]
    Returns:
        dataframe after elevation filtering
    '''
    elevation_index = (dataframe['elevation'] > elevation_mask[0]) & \
        (dataframe['elevation'] < elevation_mask[1])
    dataframe = dataframe[elevation_index]
    return dataframe
