'''
This script provides the function for plotting

Author: Ziqing Yu
Last edited on 08/02/2023
'''
from datetime import timedelta
import numpy as np
import matplotlib.pyplot as plt

# pylint:disable=invalid-name

def plot_timeseries(ts_antenne1, ts_antenne2, h_antenne_1, h_antenne_2,\
     ts_gauge, ts_sentinel, retrack_method):
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
    h_ts_0811_2 = h_antenne_1 - np.asarray(list(ts_antenne1.values()))+0.2
    h_ts_0811_3 = h_antenne_2 - np.asarray(list(ts_antenne2.values()))+0.2

    t1 = min([list(ts_antenne1.keys())[0],list(ts_antenne2.keys())[0]])-timedelta(minutes=20)
    t2 = max([list(ts_antenne1.keys())[-1],list(ts_antenne2.keys())[-1]])+timedelta(minutes=20)

    date = t1.day
    month = t2.month
    plt.rcParams.update({'font.size': 10})
    fig,ax = plt.subplots()
    datekey = f'{date}{month}'

    # plot height
    legend = ['GNSS antenne 1','GNSS antenne 2']
    ax.scatter(list(ts_antenne1.keys()), list(h_ts_0811_2), s=1)
    ax.scatter(list(ts_antenne2.keys()), list(h_ts_0811_3), s=1)
    if ts_gauge:
        ax.scatter(list(ts_gauge.keys()), list(ts_gauge.values()), s=10,color='black')
        legend.append('Gauge')
    if ts_sentinel:
        ax.scatter(list(ts_sentinel.keys()), list(ts_sentinel.values()), s=10)
        legend.append(retrack_method)
    ax.set_xlabel('time')
    ax.set_ylabel('heihgt [meter]')
    ax.set_title(\
        f'water surface height {date}.{month} (elevation 10-30, time window 30 minutes)')
    ax.set_xlim([t1,t2])
    ax.set_ylim([283.5,285.5])
    ax.grid()
    ax.legend(legend)

    fig.set_size_inches(10,4)
    fig.savefig(f'../../write/bilder/kapitel4/timeseries{datekey}.png')

def plot_timeseries_0216(ts_antenne1, ts_antenne2, h_antenne_1, h_antenne_2):
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
    h_ts_0811_2 = h_antenne_1 - np.asarray(list(ts_antenne1.values()))
    h_ts_0811_3 = h_antenne_2 - np.asarray(list(ts_antenne2.values()))
    t1 = ts_antenne1.keys()[0]-timedelta(minutes=20)
    t2 = ts_antenne1.keys()[-1]+timedelta(minutes=20)
    # plot all
    plt.rcParams.update({'font.size': 10})
    fig,ax = plt.subplots()
    ax.scatter(list(ts_antenne1.keys()), list(h_ts_0811_2), s=1)
    ax.scatter(list(ts_antenne2.keys()), list(h_ts_0811_3), s=1)
    ax.set_xlabel('time (date hour:minute)')
    ax.set_ylabel('heihgt(meter)')
    ax.set_title(f'water surface height {16}.{2} (elevation 5-30, time window 30 minutes)')
    ax.set_xlim([t1,t2])
    ax.set_ylim([283,285])
    ax.legend(['gnss antenne 1','gnss antenne 2'])
    fig.set_size_inches(9,2)
    fig.savefig('picture/timeseries0216.png')
