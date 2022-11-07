import random
import os
import pandas as pd

if __name__ == "__main__":
    gnss_sate_name = []
    gnss_color = []
    for i in range(32):
        gnss_sate_name.append(f'G{i+1}')
        gnss_color.append(["#"+"".join([random.choice("0123456789ABCDEF") for j in range(6)])])
    for i in range(24):
        gnss_sate_name.append(f'R{i+1}')
        gnss_color.append(["#"+"".join([random.choice("0123456789ABCDEF") for j in range(6)])])
    for i in range(30):
        gnss_sate_name.append(f'E{i+1}')
        gnss_color.append(["#"+"".join([random.choice("0123456789ABCDEF") for j in range(6)])])

    gnss_sate_color = pd.DataFrame({"color":gnss_color},index=gnss_sate_name)
    path = os.path.abspath("../data/color/")
    gnss_sate_color.to_csv(f"{path}\\\\gnss_color.csv")