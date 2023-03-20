"""
This script uses teqc to generate the rinex n/o file and
the compact file for snr, elevation and azimut.

Author: Ziqing Yu
Last edited on 13/06/2022
"""
import os

def call_teqc(raw_data, receiver_arg, main_result_name, time_arg):
    """
    this function calls teqc.exe
    Arg:
        raw_data: full name of the GNSS raw data

    """
    teqc_path = os.path.abspath('../../tool/teqc.exe')

    target_folder = os.path.dirname(raw_data)
    main_result_name = target_folder + main_result_name


    add_obs_arg = f"+obs {main_result_name}.22o"
    add_nav_arg = f"+nav {main_result_name}.22n,{main_result_name}.22g,{main_result_name}.22d,{main_result_name}.22l"

    teqc_generate_rinex_command = f"{teqc_path} {receiver_arg} {time_arg} {add_obs_arg} {add_nav_arg} +C2 +L5 +L6 +L7 +L8 {raw_data}"
    print(teqc_generate_rinex_command)
    os.system(teqc_generate_rinex_command)

    teqc_generate_compact_commad = teqc_path + " +qc +plot -nav " + main_result_name +\
        ".22n,"+ main_result_name + ".22g,"+ main_result_name + ".22l" + " " +\
            main_result_name + ".22o" + " > " + main_result_name + ".qcq"
    os.system(teqc_generate_compact_commad)
