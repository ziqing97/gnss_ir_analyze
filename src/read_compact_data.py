"""
This script extracts the data from file with
.sn1, .sn2, .ele, .azi extended filename, which
are generated from teqc.

Author: Ziqing Yu
generated on 05/03/2023
last edited on 05/03/2023
"""
from datetime import datetime,timezone,timedelta
import os
import numpy as np

def read_compact_data(file_name):
    """
    This script extracts the data from file with
    .sn1, .sn2, .ele, .azi extended filename, which
    are generated from teqc.
    Args:
        file_name: (str) file fullname
    Returns:
        return a dictionary of the data grouped by
        satellite
    """
    # get the data_type
    data_type = file_name[-3:]
    if data_type == 'ele' or data_type == 'azi':
        pass
    else:
        data_type = f'{file_name[-3:-1]}r{file_name[-1]}'
    # init satellite list
    data_dict = {}

    file = open(file_name, "r", encoding='utf8')

    file_line = file.readline()
    file_line = file.readline()

    # get start time
    start_time = datetime(int(file_line[15:19]),int(file_line[20:22]),int(file_line[23:25])\
        ,int(file_line[26:28]),int(file_line[29:31]),int(file_line[32:34]),tzinfo=timezone.utc)

    # read data by line
    satellite_list_temp = []
    file_line = file.readline()
    while file_line:
        line_head = file_line.split()
        delta_time_string = timedelta(seconds=float(line_head[0]))
        if int(line_head[1]) != -1:
            satellite_count = int(line_head[1])
            satellite_list_temp = []
            for i in range(2,satellite_count+2):
                satellite_list_temp.append(line_head[i])
                if not line_head[i] in data_dict:
                    data_dict[line_head[i]]={}
                    data_dict[line_head[i]]["time"] = []
                    data_dict[line_head[i]][data_type] = []
        file_line = file.readline()
        data_list = file_line.split()
        for i in range(0,satellite_count):
            data_dict[satellite_list_temp[i]][data_type].append(float(data_list[i]))
            data_dict[satellite_list_temp[i]]["time"].append(start_time+delta_time_string)
        file_line = file.readline()

    # close file
    file.close()

    # converse data to numpy array
    for key,value in data_dict.items():
        data_dict[key][data_type] = np.asarray(value[data_type])
    return data_dict

def generate_database(main_path):
    """
    This script reads all 4 necessary compact file
    and returns all result in a dict
    Args:
        main_path: the path where the files exist
    Returns:
        A dictionary which stores all ele, azi, sn1
        and sn2 data.
    """
    main_path = main_path+'/'
    file_list = os.listdir(main_path)
    data_list = {}
    for item in file_list:
        file_ext = os.path.splitext(item)
        ext = file_ext[1]
        if ext == '.sn1':
            sn1_file = main_path + item
            sn1_data = read_compact_data(sn1_file)
            data_list['snr1'] = sn1_data
        if ext == '.sn2':
            sn2_file = main_path + item
            sn2_data = read_compact_data(sn2_file)
            data_list['snr2'] = sn2_data
        if ext == '.sn5':
            sn5_file = main_path + item
            sn5_data = read_compact_data(sn5_file)
            data_list['snr5'] = sn5_data
        if ext == '.sn7':
            sn7_file = main_path + item
            sn7_data = read_compact_data(sn7_file)
            data_list['snr7'] = sn7_data
        if ext == '.sn8':
            sn8_file = main_path + item
            sn8_data = read_compact_data(sn8_file)
            data_list['snr8'] = sn8_data
        if ext == '.ele':
            ele_file = main_path + item
            ele_data = read_compact_data(ele_file)
            data_list['ele'] = ele_data
        if ext == '.azi':
            azi_file = main_path + item
            azi_data = read_compact_data(azi_file)
            data_list['azi'] = azi_data
    return data_list
    