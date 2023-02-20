'''
This script generates for each satellite a pands
dataframe and filters the data so that they are in
a right elevation and azimut range

Author: Ziqing Yu
Last edited on 13/06/2022
'''

from datetime import datetime, timedelta
import pandas as pd
import read_compact_data as rcd

# pylint:disable=invalid-name

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
    sn5_data = data_dict['sn5']
    sn7_data = data_dict['sn7']
    sn8_data = data_dict['sn8']

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
            df_snr2 = pd.DataFrame({'time':[],'snr2':[]})

        if satellite_code in sn5_data:
            df_snr5 = pd.DataFrame({'time':sn5_data[satellite_code]['time'],\
                'snr5':sn5_data[satellite_code]['sn5']})
        else:
            df_snr5 = pd.DataFrame({'time':[],'snr5':[]})

        if satellite_code in sn7_data:
            df_snr7 = pd.DataFrame({'time':sn7_data[satellite_code]['time'],\
                'snr7':sn7_data[satellite_code]['sn7']})
        else:
            df_snr7 = pd.DataFrame({'time':[],'snr7':[]})

        if satellite_code in sn8_data:
            df_snr8 = pd.DataFrame({'time':sn8_data[satellite_code]['time'],\
                'snr8':sn8_data[satellite_code]['sn8']})
        else:
            df_snr8 = pd.DataFrame({'time':[],'snr8':[]})

        dataframe = pd.merge(df_azimut,df_elevation,on=['time'],how='left')
        dataframe = pd.merge(dataframe,df_snr1,on=['time'],how='left')
        dataframe = pd.merge(dataframe,df_snr2,on=['time'],how='left')
        dataframe = pd.merge(dataframe,df_snr5,on=['time'],how='left')
        dataframe = pd.merge(dataframe,df_snr7,on=['time'],how='left')
        dataframe = pd.merge(dataframe,df_snr8,on=['time'],how='left')
        dataframe_dict[satellite_code] = dataframe
    return dataframe_dict

def azimut_filter(dataframe:pd.DataFrame,azimut_mask:list) -> pd.DataFrame:
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
    index = dataframe['azimut'] < 0
    dataframe.loc[index,'azimut'] = dataframe.loc[index,'azimut']+360

    if azimut_mask[0] < azimut_mask[1]:
        azimut_index = (dataframe['azimut'] > azimut_mask[0]) & \
            (dataframe['azimut'] < azimut_mask[1])
    else:
        azimut_index = (dataframe['azimut'] > azimut_mask[0]) | \
            (dataframe['azimut'] < azimut_mask[1])
    dataframe = dataframe[azimut_index]
    return dataframe

def elevation_filter(dataframe:pd.DataFrame,elevation_mask:list) -> pd.DataFrame:
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

def sn1_filter(dataframe:pd.DataFrame) -> pd.DataFrame:
    """
    this function filter out the data without L1 snr
    Args:
        dataframe (pd.DataFrame): dataframe generated from 'generate dataframe'

    Returns:
        pd.DataFrame: same as input, the invalid data outfiltered
    """
    dataframe = dataframe[dataframe['snr1'].notnull()]
    return dataframe

def clean_data(main_path:str, elevation_mask:list,\
    azimut_mask:list, sn1_trigger:bool)->pd.DataFrame:
    """
    this function does the necessary filtering for the data
    Args:
        main_path (_type_): where all compactfiles exist
        elevation_mask (list): a list with 2 elements [min, max]
        azimut_mask (list): a list with 2 elements [min, max] in clockwise
                     direction
        sn1_trigger (bool): if the snr1 nan should be filtered out
    """
    data_dict = generate_dataframe(main_path)
    data_empty_code = []
    satellite_list = data_dict.keys()
    for satellite_code in satellite_list:
        data_dict[satellite_code] = azimut_filter(data_dict[satellite_code],azimut_mask)
        data_dict[satellite_code] = elevation_filter(data_dict[satellite_code],elevation_mask)
        if sn1_trigger:
            data_dict[satellite_code] = sn1_filter(data_dict[satellite_code])
        if data_dict[satellite_code].empty:
            data_empty_code.append(satellite_code)

    for satellite_code in data_empty_code:
        del data_dict[satellite_code]
    return data_dict

def split_data(data_dict:pd.DataFrame,starttime:datetime,\
    endtime:datetime,deltatime:timedelta)->dict:
    """
    this function split the whole dataset in to small parts in certain time intervals
    Args:
        data_dict (pd.DataFrame): _description_
        starttime (datetime): _description_
        endtime (datetime): _description_
        deltatime (timedelta): _description_

    Returns:
        dict: _description_
    """
    time_list = [starttime]
    while time_list[-1] < endtime:
        time_list.append(time_list[-1]+deltatime)
    df_time = pd.DataFrame({'time_tick':time_list})

    satellite_list = list(data_dict.keys())
    split_data_dict = {}
    for satellite_code in satellite_list:
        dataframe = data_dict[satellite_code]
        temp_list = []
        temp_time_list = []
        split_data_dict[satellite_code] = {}
        for i in range(0,len(df_time)-1):
            t1 = df_time.iloc[i]['time_tick']
            t2 = df_time.iloc[i+1]['time_tick']
            df_temp = dataframe[(pd.to_datetime(dataframe['time'])>t1)\
                & (pd.to_datetime(dataframe['time'])<=t2)]

            ###
            df_ele = list(df_temp['elevation'])
            if all(x<=y for x, y in zip(df_ele[0:-1], df_ele[1:])) or \
               all(x>=y for x, y in zip(df_ele[0:-1], df_ele[1:])):
            ###
                if df_temp.shape[0]==deltatime.seconds:
                    temp_list.append(df_temp)
                    temp_time_list.append(t1+deltatime/2)
        split_data_dict[satellite_code]['raw'] = temp_list
        split_data_dict[satellite_code]['time'] = temp_time_list
    return split_data_dict
