'''
This script provides the function for plotting

Author: Ziqing Yu
Last edited on 08/02/2023
'''
from datetime import datetime,timezone
import numpy as np
import matplotlib.pyplot as plt

# pylint:disable=invalid-name

def plot_timeseries(ts_antenne1, ts_antenne2, h_antenne_1, h_antenne_2,\
     ts_gauge, ts_sentinel, retrack_method, datekey):
    """
    This function plots the timeseries together.
    Args:
        ts_antenne1 (_type_): _description_
        ts_antenne2 (_type_): _description_
        h_antenne_1 (_type_): _description_
        h_antenne_2 (_type_): _description_
        ts_gauge (_type_): _description_
        ts_sentinel (_type_): _description_
        retrack_method (_type_): _description_
        datekey (_type_): _description_
    """
    month = int(datekey[0:2])
    date = int(datekey[2:])
    h_ts_0811_2 = h_antenne_1 - np.asarray(list(ts_antenne1.values()))
    h_ts_0811_3 = h_antenne_2 - np.asarray(list(ts_antenne2.values()))
    # plot all
    plt.rcParams.update({'font.size': 10})
    fig,ax = plt.subplots()
    ax.scatter(list(ts_antenne1.keys()), list(h_ts_0811_2), s=1)
    ax.scatter(list(ts_antenne2.keys()), list(h_ts_0811_3), s=1)
    ax.scatter(list(ts_gauge.keys()), list(ts_gauge.values()), s=10)
    ax.scatter(list(ts_sentinel.keys()), list(ts_sentinel.values()), s=10)
    ax.set_xlabel('time (date hour:minute)')
    ax.set_ylabel('heihgt(meter)')
    ax.set_title(f'water surface height {date}.{month} (elevation 5-30, time window 30 minutes)')
    ax.set_xlim([datetime(year=2022,month=month,day=date,hour=8,\
            minute=30,second=0,tzinfo=timezone.utc),\
                datetime(year=2022,month=month,day=date,hour=11,\
            minute=0,second=0,tzinfo=timezone.utc)])
    ax.set_ylim([283,285])
    ax.legend(['gnss antenne 1','gnss antenne 2','gauge',retrack_method])
    fig.set_size_inches(9,2)
    fig.savefig(f'picture/timeseries{datekey}.png')
