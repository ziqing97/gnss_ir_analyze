"""
main function for GNSS-R analysis

Author: Ziqing Yu
Last edited on 13/06/2022
"""

import PySimpleGUI as sg
from generate_rinex_compact import call_teqc

def gnss_ir_gui():
    '''
    GUI Framework
    '''
    # gui layout for generate rinex and compact
    layout = [[sg.Input("E:/OneDrive/Studium/MA/gnss_ir_analyze/data/20221127/2/5856_1127_094935.m00",\
                key='raw_data'),sg.FileBrowse('raw_data',key='raw_data')],
            [sg.Text('Please give a rough measuring time')],
            [sg.Text('year'),sg.InputText('2022',key='year', size=(4,1)),sg.Text('month'),\
                sg.InputText('05',key='month', size=(2,1)),\
                sg.Text('day'),sg.InputText('26',key='day', size=(2,1))],
            [sg.Text('from'),sg.InputText('19',key='hour1', size=(2,1)),sg.Text('o\'clock'),\
                sg.Text('to'),sg.InputText('22',key='hour2', size=(2,1)),sg.Text('o\'clock')],
            [sg.Text('Please give the receiver type argument'),\
                sg.InputText('-leica mdb',key='receiver_type')],
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
    main_result_name = '/' + year + month + day
    hour_begin = values['hour1']
    hour_end = values['hour2']
    receiver_arg = values['receiver_type']
    time_arg = '-st '+year+'_'+month+'_'+day+':'+hour_begin+':00:00'+\
        ' -e '+year+'_'+month+'_'+day+':'+hour_end+':00:00'
    call_teqc(raw_data, receiver_arg, main_result_name, time_arg)

if __name__ == "__main__":
    main()
