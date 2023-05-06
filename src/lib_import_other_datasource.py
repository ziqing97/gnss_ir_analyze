"""_summary_
"""
import pickle
from datetime import datetime,timezone
import pandas as pd

# pylint:disable=invalid-name
def get_antenne_height(key):
    """_summary_

    Args:
        key (str): _description_

    Returns:
        dict: antenne height dictionary
    """
    with open('../data/generated_data/antenne_height.pkl', 'rb') as f:
        df_ante_h = pickle.load(f)
    ante_h = {}
    index = df_ante_h[df_ante_h['date'] == key]
    if key == '0216':
        ante_h['1'] = float(index['antenne1'])
        ante_h['2'] = float(index['antenne2'])+0.2
        ante_h['2r'] = float(index['antenne2r'])
    elif key[0:-2] == '0315':
        ante_h['1'] = float(index['antenne1'])
        ante_h['r'] = float(index['antenne2r'])
    else:
        ante_h['2'] = float(index['antenne2'])+0.2
        ante_h['3'] = float(index['antenne3'])+0.2
    return ante_h

def get_gauge_data(date_key):
    """_summary_

    Args:
        date_key (_type_): _description_

    Returns:
        _type_: _description_
    """
    ts_gauge = pd.read_csv(f'../data/gauge/2022{date_key}_gauge.csv')
    ts_gauge_reform = {}
    for t,h in zip(ts_gauge['0'],ts_gauge['1']):
        ts_gauge_reform[datetime.fromtimestamp(t,tz=timezone.utc)] = h
    return ts_gauge_reform

def get_sentinel_data(date_key,method):
    """_summary_

    Args:
        date_key (_type_): _description_
        method (_type_): _description_

    Returns:
        _type_: _description_
    """
    ts_sentinel = {}
    df_sentinel = pd.read_csv(f'../data/altbundle/2022{date_key}sentinel.csv')
    for t,h in zip(df_sentinel['unixtime'],df_sentinel[method]):
        ts_sentinel[datetime.fromtimestamp(t,tz=timezone.utc)] = h
    return ts_sentinel
