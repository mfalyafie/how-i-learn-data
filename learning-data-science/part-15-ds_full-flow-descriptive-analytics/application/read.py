"""
    m.fauzanalyafie@gmail.com
    31-Agustus-2022 13:58
"""

import pandas as pd #type: ignore


class Read:
    
    def stock_market(self):

        df_stock         = pd.read_csv("./data/NIFTY 50 - HistoricalPE_PBDIV_Data.csv")

        return df_stock