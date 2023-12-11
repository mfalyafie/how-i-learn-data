"""
    m.fauzanalyafie@gmail.com
    20-Agustus-2022 13:09 PM
"""

import numpy as np #type: ignore
import pandas as pd #type: ignore
import seaborn as sns #type: ignore
from pandas_profiling import ProfileReport #type: ignore
import matplotlib.pyplot as plt #type:ignore
from sklearn.impute import SimpleImputer #type: ignore
from . read import Read


class Eda:


    def stats(self):
        
        # read data
        df_indeks = Read.read_csv(self)

        # print data
        print(df_indeks.head())
        print("------")

        # find any null value
        print(df_indeks.isnull().any())

        # replace to correct null/NaN values
        df_indeks.replace('---', np.nan, inplace = True)        

        # transform data type
        df_indeks[["pm10", "so2", 'co', 'o3', 'no2', 'max']] = df_indeks[[
            "pm10", "so2", 'co', 'o3', 'no2', 'max']].apply(pd.to_numeric)

        imputer = SimpleImputer(missing_values=np.nan, strategy="median")
        imputer.fit(df_indeks[["pm10", "so2", 'co', 'o3', 'no2', 'max']])
        df_indeks[["pm10", "so2", 'co', 'o3', 'no2', 'max']] = imputer.transform(
            df_indeks[["pm10", "so2", 'co', 'o3', 'no2', 'max']])

        # find information for all columns
        print("General info:\n", df_indeks.info())
        print("------")


        # print descriptive statistics of the data
        print("Descriptive statistics:\n", df_indeks.describe())
        print("------")

        # print additional descriptive statistics
        
        print("Median:\n", df_indeks.median(numeric_only = True))
        print("------")

        print("Mode:\n", df_indeks.mode(numeric_only = True))
        print("------")

        print("Skewness:\n", df_indeks.skew(numeric_only = True))
        print("------")        

        # create eda plot
        # set color
        sns.set_style("darkgrid")

        try:
            
            fig, axs = plt.subplots(3, 2, figsize=(40, 20))

            sns.violinplot(data=df_indeks, x="stasiun", y='pm10', ax=axs[0, 0])
            sns.violinplot(data=df_indeks, x="stasiun", y='so2', ax=axs[0, 1])
            sns.violinplot(data=df_indeks, x="stasiun", y='co', ax=axs[1, 0])
            sns.violinplot(data=df_indeks, x="stasiun", y='o3', ax=axs[1, 1])
            sns.violinplot(data=df_indeks, x="stasiun", y='no2', ax=axs[2, 0])
            sns.violinplot(data=df_indeks, x="stasiun", y='max', ax=axs[2, 1])

            # save box plot
            plt.savefig("./chart/violinplot_pencemaran.png")

            # clear current fig
            plt.cla()

            # print status
            print("success save image")

        except:

            print("cannot save image")

        try:

            # profiling dataset
            profile_data_indeks        = ProfileReport(df_indeks, title="Indeks Pencemaran Profiling")

            # save data
            profile_data_indeks.to_file("./profiling/indeks_pencemaran_profiling.html")

            print("success save profiling")

        except:

            print("cannot save")
        