"""
This script uses teqc to generate the rinex n/o file and
the compact file for snr, elevation and azimut.
"""
import os

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
