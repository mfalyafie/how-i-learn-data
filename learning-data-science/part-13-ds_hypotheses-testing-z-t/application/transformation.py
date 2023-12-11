"""
    m.fauzanalyafie@gmail.com
    27-Agustus-2022 18:01
"""

# import  necessary libraries
import pandas as pd #type: ignore
from scipy.stats import zscore #type: ignore
import scipy.stats as st #type: ignored
import numpy as np #type: ignore
from . read import Read

class Transformation:

    def t_test(self):

        # read the daily activity csv to dataframe
        df_da = Read.daily_activity(self)

        df_da_calories = df_da[df_da['Calories'] != 0]['Calories']

        # if data <= 30 100% population
        if len(df_da_calories) <= 30:
            df_cal_sample =  df_da_calories
        # if data > 30 and <= 100 50% population
        elif (len(df_da_calories) > 30) and (len(df_da_calories) <= 100):
            df_cal_sample =  df_da_calories.sample(n=round(0.5*len(df_da_calories)))         
        # if data > 100 and < 1000 30% population
        elif (len(df_da_calories) > 100) and (len(df_da_calories) < 1000):
            df_cal_sample =  df_da_calories.sample(n=round(0.3*len(df_da_calories)))    
        # if data >= 1000 10% population : mendekatai 1000 tetap 10%
        else:
            df_cal_sample =  df_da_calories.sample(n=round(0.1*len(df_da_calories)))

        # print number of samples used
        print('number of samples used: {}'.format(len(df_cal_sample)))
        print('=================================================')
        
        # if len data < 30 t test
        if len(df_cal_sample) < 30:
            ci_cal = st.t.interval(
                                    alpha=0.95,
                                    df   = len(df_cal_sample)-1,
                                    loc  = np.mean(df_cal_sample),
                                    scale= st.sem(df_cal_sample)
                        )
        # elif len data >= 30 z test 
        else:
            ci_cal = st.norm.interval(
                                    alpha=0.95,
                                    loc  = np.mean(df_cal_sample),
                                    scale= st.sem(df_cal_sample)
                        )

        print('Mean:{}'.format(np.mean(df_cal_sample)))
        print('Confidence Interval: {}'.format(ci_cal))
        print('Population Mean: {}'.format(np.mean(df_da_calories)))