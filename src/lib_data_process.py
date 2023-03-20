"""
This script does the calculation of the gnss-ir
analyse

"""
from datetime import timedelta

from scipy import signal
import numpy as np

import lib_data_filter as dafi

# pylint:disable=invalid-name,consider-using-dict-items

C = 299792458 # m/s
FREQUENCY_GPS_L1 = 1575.42 * 10**6
WAVELENTH_GPS_S1 = C/FREQUENCY_GPS_L1

FREQUENCY_GPS_L2 = 1227.6 * 10**6
WAVELENTH_GPS_S2 = C/FREQUENCY_GPS_L2

FREQUENCY_GPS_L5 = 1176.45 * 10**6
WAVELENTH_GPS_S5 = C/FREQUENCY_GPS_L5

# Glonass
FREQUENCY_GLONASS_L1 = 1602 * 10**6
WAVELENTH_GLONASS_S1 = C/FREQUENCY_GLONASS_L1

FREQUENCY_GLONASS_L2 = 1246 * 10**6
WAVELENTH_GLONASS_S2 = C/FREQUENCY_GLONASS_L2

# Galileo
FREQUENCY_GALILEO_L5 = 1176.45 * 10**6
WAVELENTH_GALILEO_S5 = C/FREQUENCY_GALILEO_L5

FREQUENCY_GALILEO_L6 = 1278.7 * 10**6
WAVELENTH_GALILEO_S6 = C/FREQUENCY_GALILEO_L6

FREQUENCY_GALILEO_L7 = 1207.140 * 10**6
WAVELENTH_GALILEO_S7 = C/FREQUENCY_GALILEO_L7

FREQUENCY_GALILEO_L8 = 1191.795 * 10**6
WAVELENTH_GALILEO_S8 = C/FREQUENCY_GALILEO_L8

class libDataProcess():
    """
    class document
    """
    def __init__(self) -> None:
        self.power_list = {'snr1':[],'snr2':[],'snr5':[],'snr7':[],'snr8':[]}

    def calc_lsp_power(self,elevation_sort,snr_sort,frequency,wavelength):
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

    def extract_azimut(self,azimut_array):
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

    def extract_elevation(self,elevation_array):
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

    def generate_frequency(self,min_height,max_height):
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

    def get_wavelength(self,snr_type, satellite_code):
        """
        Return the carrier wavelength acoording to
        the satellite system and carrier type
        Args:
            snr_type (_type_): _description_
            satellite_code (_type_): _description_

        Returns:
            _type_: _description_
        """
        glonass_list = {'14':-7,'15':0,'10':-7,'20':2,'19':3,'13':-2,\
                             '12':-1,'01':1,'06':-4,'05':1,'22':-3,'23':3,\
                             '24':2,'16':-1,'04':6,'08':6,'03':5,'07':5,\
                             '02':-4,'18':-3,'21':4,'09':-2,'17':4,'11':0}
        if snr_type == 'snr1':
            if satellite_code[0]=='R':
                frequency_base = FREQUENCY_GLONASS_L1
                pnr = satellite_code[1:]
                channel = glonass_list[pnr]
                frequency_glo = frequency_base + channel * 0.5625 * 10**6
                wavelength = C / frequency_glo
            elif (satellite_code[0]=='G') or (satellite_code[0]=='E'):
                wavelength = WAVELENTH_GPS_S1
            else:
                wavelength = None
        elif snr_type == 'snr2':
            if satellite_code[0]=='R':
                frequency_base = FREQUENCY_GLONASS_L2
                pnr = satellite_code[1:]
                channel = glonass_list[pnr]
                frequency_glo = frequency_base + channel * 0.4375 * 10**6
                wavelength = C / frequency_glo
            elif satellite_code[0]=='G':
                wavelength = WAVELENTH_GPS_S2
            else:
                wavelength = None
        elif snr_type == 'snr5':
            if satellite_code[0]=='E':
                wavelength = WAVELENTH_GALILEO_S5
            elif satellite_code[0]=='G':
                wavelength = WAVELENTH_GPS_S5
            else:
                wavelength = None
        elif snr_type == 'snr7':
            if satellite_code[0]=='E':
                wavelength = WAVELENTH_GALILEO_S7
            else:
                wavelength = None
        elif snr_type == 'snr8':
            if satellite_code[0]=='E':
                wavelength = WAVELENTH_GALILEO_S8
            else:
                wavelength = None
        return wavelength

    def data_prepare(self,split_data_dict,frequency):
        """
        this function does all the necessary things

        Args:
            split_data_dict (_type_): _description_
            min_height (_type_): _description_
            max_height (_type_): _description_

        Returns:
            _type_: _description_
        """
        split_data_dict_copy=split_data_dict
        for snr_type in split_data_dict_copy:
            for satellite_code in split_data_dict_copy[snr_type]:
                # init the list for power
                split_data_dict_copy[snr_type][satellite_code]['power'] = []
                split_data_dict_copy[snr_type][satellite_code]['elevation'] = []
                split_data_dict_copy[snr_type][satellite_code]['azimut'] = []
                wavelength = self.get_wavelength(snr_type, satellite_code)
                if wavelength is None:
                    continue

                # a loop to calculate the power
                for item in split_data_dict_copy[snr_type][satellite_code]['raw']:
                    # sort data by elevation
                    dataframe_sort = item.sort_values(by='elevation')

                    # get the elevation and azimut information
                    ele_dict = self.extract_azimut(dataframe_sort.loc[:]['elevation'])
                    azi_dict = self.extract_azimut(dataframe_sort.loc[:]['azimut'])
                    split_data_dict_copy[snr_type][satellite_code]['elevation'].append(ele_dict)
                    split_data_dict_copy[snr_type][satellite_code]['azimut'].append(azi_dict)

                    # do the lsp analyse
                    elevation_sort = np.array([dataframe_sort['elevation']]).T
                    snr_sort = np.array([dataframe_sort[snr_type]]).T
                    power = self.calc_lsp_power(elevation_sort,snr_sort,frequency,wavelength)
                    if np.max(power)>0.1:
                        split_data_dict_copy[snr_type][satellite_code]['power'].append(power)
                    else:
                        split_data_dict_copy[snr_type][satellite_code]['power'].append(np.array([]))
        return split_data_dict_copy

    def extract_height(self,signal_ts,frequency,max_height,min_height):
        """_summary_

        Args:
            signal_ts (_type_): _description_
            frequency (_type_): _description_
            max_height (_type_): _description_
            min_height (_type_): _description_

        Returns:
            _type_: _description_
        """
        height_ts = {}
        for t in signal_ts:
            p = signal_ts[t]
            index = (frequency<=max_height) & (frequency>=min_height)
            frequency0 = frequency[index]
            p0 = p[index]

            index_peak, _ = signal.find_peaks(p0)
            if index_peak.size != 0:
                p_inpeak = p0[index_peak]
                f_inpeak = frequency0[index_peak]
                index_max = p_inpeak==max(p_inpeak)
                h = f_inpeak[index_max]
                height_ts[t] = h[0]
            else:
                height_ts[t] = np.nan
        return height_ts

    def generate_timeseries(self,main_path, azimut_mask, elevation_mask, \
        min_height, max_height, t_range, starttime, endtime, trigger_list, sample_rate):
        """
        Args:
            main_path (_type_): _description_
            azimut_mask (_type_): _description_
            elevation_mask (_type_): _description_
            min_height (_type_): _description_
            max_height (_type_): _description_
            t_range (_type_): _description_

        Returns:
            _type_: _description_
        """
        frequency = self.generate_frequency(min_height=min_height,max_height=max_height*3)
        signal_ts = {}
        count_ts = {}
        for dt in range(0,t_range):
            starttime_split = starttime + timedelta(minutes=dt)
            endtime_split = endtime + timedelta(minutes=dt)
            deltatime = timedelta(minutes=t_range)
            split_data_dict = {}
            for snr_trigger in trigger_list:
                data_dict = dafi.clean_data(main_path,azimut_mask=azimut_mask,\
                    elevation_mask=elevation_mask,trigger=snr_trigger)
                split_data_dict[snr_trigger] = \
                    dafi.split_data(data_dict,starttime_split,endtime_split,\
                                    deltatime,sample_rate=sample_rate)

            result_dict = self.data_prepare(split_data_dict,frequency=frequency)
            for snr_type in result_dict:
                for satellite_code in result_dict[snr_type]:
                    for t,p in zip(result_dict[snr_type][satellite_code]['time'],\
                        result_dict[snr_type][satellite_code]['power']):
                        if p.any():
                            self.power_list[snr_type].append(p)
                            if t in signal_ts:
                                signal_ts[t] = np.multiply(p,signal_ts[t])
                                count_ts[t] = count_ts[t]+1
                            else:
                                signal_ts[t] = p
                                count_ts[t] = 1
        height_ts = self.extract_height(signal_ts,frequency,max_height,min_height)
        return height_ts,count_ts
