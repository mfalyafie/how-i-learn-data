"""
    m.fauzanalyafie@gmail.com
    24-Agustus-2022 17:58 PM
"""

import pandas as pd #type: ignore


class Read:


    def cars_csv(self):

        df_cars         = pd.read_csv("./data/cars_raw.csv")

        return df_cars