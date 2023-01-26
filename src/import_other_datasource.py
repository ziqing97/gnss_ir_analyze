"""_summary_
"""
import pickle
from datetime import datetime,timezone
import pandas as pd

# pylint:disable=invalid-name
def get_antenne_height(key):
    """_summary_

    Args:
        key (_type_): _description_

    Returns:
        _type_: _description_
    """
    with open('../data/generated_data/antenne_height.pkl', 'rb') as f:
        df_ante_h = pickle.load(f)
    ante_h = {}
    index = df_ante_h[df_ante_h['date'] == key]
    ante_h['2'] = float(index['antenne2'])
    ante_h['3'] = float(index['antenne3'])
    return ante_h

def get_gauge_data(date_key):
    """_summary_

    Args:
        date_key (_type_): _description_

    Returns:
        _type_: _description_
    """
    ts_gauge = pd.read_csv(f'../data/gauge/2022{date_key}_gauge.csv')
    gauge_time = []
    h_ts_gauge = []
    for t,h in zip(ts_gauge['0'],ts_gauge['1']):
        gauge_time.append(datetime.fromtimestamp(t,tz=timezone.utc))
        h_ts_gauge.append(h)
    return gauge_time,h_ts_gauge

def get_sentinel_data(date_key,method):
    """_summary_

    Args:
        date_key (_type_): _description_
        method (_type_): _description_

    Returns:
        _type_: _description_
    """
    sentinel_time = []
    h_ts_sentinel = []
    df_sentinel = pd.read_csv(f'../data/altbundle/2022{date_key}sentinel.csv')
    for t,h in zip(df_sentinel['unixtime'],df_sentinel[method]):
        sentinel_time.append(datetime.fromtimestamp(t,tz=timezone.utc))
        h_ts_sentinel.append(h)
    return sentinel_time,h_ts_sentinel
