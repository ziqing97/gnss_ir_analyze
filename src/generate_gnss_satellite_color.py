"""
This Script generates a csv file which documents all the satellites' color
"""
import random
import os
import pandas as pd

if __name__ == "__main__":
    gnss_sate_name = []
    gnss_color = []
    for i in range(32):
        if i>8:
            gnss_sate_name.append(f'G{i+1}')
        else:
            gnss_sate_name.append(f'G0{i+1}')
        color = ["#"+"".join([random.choice("0123456789ABCDEF") for j in range(6)])]
        gnss_color.append(color[0])
    for i in range(24):
        if i>8:
            gnss_sate_name.append(f'R{i+1}')
        else:
            gnss_sate_name.append(f'R0{i+1}')
        color = ["#"+"".join([random.choice("0123456789ABCDEF") for j in range(6)])]
        gnss_color.append(color[0])
    for i in range(33):
        if i>8:
            gnss_sate_name.append(f'E{i+1}')
        else:
            gnss_sate_name.append(f'E0{i+1}')
        color = ["#"+"".join([random.choice("0123456789ABCDEF") for j in range(6)])]
        gnss_color.append(color[0])

    gnss_sate_color = pd.DataFrame({"color":gnss_color},index=gnss_sate_name)
    path = os.path.abspath("../data/color/")
    gnss_sate_color.to_csv(f"{path}\\\\gnss_color.csv")
