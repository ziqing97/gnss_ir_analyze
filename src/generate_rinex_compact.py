"""
This script uses teqc to generate the rinex n/o file and
the compact file for snr, elevation and azimut.
"""
import os
import PySimpleGUI as sg

def call_teqc(raw_data, teqc_path, receiver_arg, main_result_name, time_arg):
    """
    this function calls teqc.exe
    Arg:
        raw_data: full name of the GNSS raw data

    """
    target_folder = os.path.dirname(raw_data)
    main_result_name = target_folder + main_result_name


    add_obs_arg = "+obs " + main_result_name + ".obs"
    add_nav_arg = "+nav " + main_result_name + ".gps,"+ main_result_name +\
        ".glo,"+ main_result_name + ".bei,"+ main_result_name + ".gal"


    teqc_generate_rinex_command = teqc_path + " " + receiver_arg + " " + time_arg + " " +\
        add_obs_arg + " " + add_nav_arg + " " + raw_data
    os.popen(teqc_generate_rinex_command)

    teqc_generate_compact_commad = teqc_path + " +qc +plus -nav " + main_result_name +\
        ".gps,"+ main_result_name + ".glo,"+ main_result_name + ".gal" + " " +\
            main_result_name + ".obs" + " > " + main_result_name + ".qcq"
    os.popen(teqc_generate_compact_commad) # somehow this doesn't work well

def gnss_ir_gui():
    '''
    a simple GUI to get the files
    '''

    # gui layout
    layout = [[sg.Input("E:/Studium/MA/software/teqc/teqc.exe",key='teqc'), \
                sg.FileBrowse('location for teqc.exe')],
            [sg.Input("E:/Studium/MA/data/20220526/2/5856_0526_213047.m00",key='raw_data'),\
                sg.FileBrowse('raw_data',key='raw_data')],
            [sg.Text('Please give a roughly beginning measuring time')],
            [sg.Text('year'),sg.InputText('2022',key='year', size=(4,1)),sg.Text('month'),\
                sg.InputText('05',key='month', size=(2,1)),\
                sg.Text('day'),sg.InputText('26',key='day', size=(2,1))],
            [sg.Text('from'),sg.InputText('19',key='hour1', size=(2,1)),sg.Text('o\'clock'),\
                sg.Text('from'),sg.InputText('22',key='hour2', size=(2,1)),sg.Text('o\'clock')],
            [sg.Text('Please give the receiver type argument'),\
                sg.InputText('-leica mdb',key='receiver_type')],
            [sg.Submit(), sg.Cancel()]]

    # open a window
    window = sg.Window('GNSS-R',layout)
    while True:
        event, value = window.read()
        if event is None or event == 'Cancel':
            break
        window.close()
        return value

def main():
    '''
    main function
    '''
    values = gnss_ir_gui()
    raw_data = values['raw_data']
    teqc_path = values['teqc']
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
    call_teqc(raw_data, teqc_path, receiver_arg, main_result_name, time_arg)

if __name__ == "__main__":
    main()
