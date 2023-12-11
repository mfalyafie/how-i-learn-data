"""
    m.fauzanalyafie@gmail.com
    28-Agustus-2022 17:11
"""

import pandas as pd #type: ignore


class Read:
    
    def advertising(self):

        df_ads         = pd.read_csv("./data/view-adv.csv")

        return df_ads