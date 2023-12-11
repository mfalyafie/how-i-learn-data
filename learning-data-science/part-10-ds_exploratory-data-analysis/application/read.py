"""
    m.fauzanalyafie@gmail.com
    20-Agustus-2022 13:09 PM
"""

import pandas as pd #type: ignore

class Read:

    def read_csv(self):

        df_data = pd.read_csv("./data/indeks-standar-pencemar-udara-di-spku-bulan-januari-tahun-2020.csv")

        return df_data