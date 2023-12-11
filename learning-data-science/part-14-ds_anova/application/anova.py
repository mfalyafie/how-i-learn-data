"""
    m.fauzanalyafie@gmail.com
    28-Agustus-2022 17:11
"""

from unittest import result
import pandas as pd #type:ignore
import numpy as np #type:ignore
from scipy.stats import f_oneway #type:ignore
from statsmodels.formula.api import ols #type:ignore
import statsmodels.api as sm #type:ignore
import seaborn as sns #type: ignore
import matplotlib.pyplot as plt #type: ignore
from . read import Read

class Anova:

    def one_way(self):

        # read the advertising data
        df_ads = Read.advertising(self)

        # use groupby so that we can easily subset the levels of each factor 
        df_ads_day = df_ads.groupby('day').view.apply(np.array)
        df_ads_time = df_ads.groupby('time').view.apply(np.array)

        # pvalue < alpha h0 ditolak
        # pvalue > alpha h0 diterima
        # h0        = tidak ada pengaruh dari kpi terhadap loyalitas  
        # h1        = ada pengaruh dari kpi terhadap loyalitas

        # one-way anova analysis for day
        print('One-way ANOVA (Day)')
        print(f_oneway(df_ads_day['weekday'], df_ads_day['weekend']))
        print('Mean comparison:')
        print('Weekday: {}'.format(np.mean(df_ads_day['weekday'])))
        print('Weekend: {}'.format(np.mean(df_ads_day['weekend'])))
        print('=================================================')

        # one-way anova analysis for time
        print('One-way ANOVA (Time)')
        print(f_oneway(df_ads_time['day'], df_ads_time['night']))
        print('Mean comparison:')
        print('Day: {}'.format(np.mean(df_ads_time['day'])))
        print('Night: {}'.format(np.mean(df_ads_time['night'])))
        print('=================================================')

        # create a plot to visualize better
        fig, axs = plt.subplots(1, 2, figsize=(30, 20))
        
        sns.barplot(x="day", y="view", data=df_ads, ax = axs[0])
        sns.barplot(x="time", y="view", data=df_ads, ax = axs[1])
        
        # save plot
        plt.savefig("./chart/oneway_advertising.png")

        # clear current fig
        plt.cla()


    def two_way(self):

        # read the advertising data
        df_ads = Read.advertising(self)

        # use groupby so that we can easily subset the levels of each factor 
        df_ads_day = df_ads.groupby('day').view.apply(np.array)
        df_ads_time = df_ads.groupby('time').view.apply(np.array)
        df_ads_day_time = df_ads.groupby(['day', 'time']).view.apply(np.array)

        # pvalue < alpha h0 ditolak
        # pvalue > alpha h0 diterima
        # h0    = tidak memiliki pengaruh
        # h1    = memiliki pengaruh

        # create the model for two-way anova
        model = ols('view ~ C(day) + C(time) +C(day):C(time)',
            data = df_ads).fit()
        result = sm.stats.anova_lm(model, type=2)

        # show the result
        print('Two-way ANOVA (Time & Day)')
        print(result)
        print('Mean combination:')
        df_ads_agg = df_ads.groupby(['day', 'time']).view.apply(np.array)
        print(df_ads_agg.apply(np.mean).to_frame().reset_index())
        print('=================================================')

        # show the plot
        fig, axs = plt.subplots(1, 1, figsize=(30, 20))
        sns.lineplot(data=df_ads, x="day", y="view", hue="time")

        # save plot
        plt.savefig("./chart/twoway_advertising.png")

        # clear current fig
        plt.cla()