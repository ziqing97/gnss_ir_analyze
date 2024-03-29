"""
main function for GNSS-R analysis

Author: Ziqing Yu
Last edited on 13/06/2022
"""

from datetime import datetime
import PySimpleGUI as sg
from generate_rinex_compact import call_teqc

def gnss_ir_gui():
    '''
    GUI Framework
    '''
    # gui layout for generate rinex and compact
    layout = [[sg.Input("",\
                key='raw_data'),sg.FileBrowse('raw_data',key='raw_data')],
            [sg.Text('Please give a rough measuring time')],
            [sg.Text('year'),sg.InputText('2023',key='year', size=(4,1)),sg.Text('month'),\
                sg.InputText('03',key='month', size=(2,1)),\
                sg.Text('day'),sg.InputText('15',key='day', size=(2,1))],
            [sg.Text('from'),sg.InputText('07',key='hour1', size=(2,1)),sg.Text('o\'clock'),\
                sg.Text('to'),sg.InputText('16',key='hour2', size=(2,1)),sg.Text('o\'clock')],
            [sg.Text('Please give the receiver type argument'),\
                sg.InputText('-lei mdb',key='receiver_type')],
            [sg.Text('Please give the stationname'),\
                sg.InputText('essr',key='station_name')],
            [sg.Submit(), sg.Cancel()]]

    # open a window
    window = sg.Window('GNSS-IR',layout)
    while True:
        event, value = window.read()
        if event is None or event == 'Cancel':
            break
        elif event =="Submit":
            print("loading successfully!")
            return value
    window.close()


def main():
    '''
    main function
    '''
    values = gnss_ir_gui()
    raw_data = values['raw_data']
    year = values['year']
    month = values['month']
    if len(month) == 1:
        month = '0'+month
    day = values['day']

    hour_begin = values['hour1']
    hour_end = values['hour2']
    receiver_arg = values['receiver_type']
    stationname = values['station_name']
    day_of_year = datetime(int(year),int(month),int(day)).timetuple().tm_yday
    if day_of_year<100:
        main_result_name = f'/{stationname}0{day_of_year}0'
    else:
        main_result_name = f'/{stationname}{day_of_year}0'
    time_arg = '-st '+year+'_'+month+'_'+day+':'+hour_begin+':00:00'+\
        ' -e '+year+'_'+month+'_'+day+':'+hour_end+':00:00'
    call_teqc(raw_data, receiver_arg, main_result_name, time_arg)

if __name__ == "__main__":
    main()
