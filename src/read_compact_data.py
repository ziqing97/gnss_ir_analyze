"""
This script extracts the data from file with
.sn1, .sn2, .ele, .azi extended filename, which
are generated from teqc.

Author: Ziqing Yu
generated on 04/06/2022
last edited on 04/06/2022
"""
from datetime import datetime,timezone,timedelta
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
    data_type = file_name[-3:-1]+file_name[-1]
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
            for i in range(2,satellite_count+1):
                satellite_list_temp.append(line_head[i])
                if not line_head[i] in data_dict:
                    data_dict[line_head[i]]={}
                    data_dict[line_head[i]]["time"] = []
                    data_dict[line_head[i]][data_type] = []
        file_line = file.readline()
        data_list = file_line.split()
        for i in range(0,satellite_count-1):
            data_dict[satellite_list_temp[i]][data_type].append(float(data_list[i]))
            data_dict[satellite_list_temp[i]]["time"].append(start_time+delta_time_string)
        file_line = file.readline()
    # close file
    file.close()
    # converse data to numpy array
    for key,value in data_dict.items():
        data_dict[key][data_type] = np.asarray(value[data_type])
    return data_dict
