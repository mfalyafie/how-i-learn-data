"""
    m.fauzanalyafie@gmail.com
    27-Agustus-2022 18:01
"""

import pandas as pd #type: ignore


class Read:
    
    def daily_activity(self):

        df_da         = pd.read_csv("./data/dailyActivity_merged.csv")

        return df_da