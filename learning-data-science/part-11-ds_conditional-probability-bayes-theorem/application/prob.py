"""
    m.fauzanalyafie@gmail.com
    23-Agustus-2022 18:21 PM
"""

from logging.handlers import DEFAULT_TCP_LOGGING_PORT
from xml.sax import default_parser_list
import pandas as pd #type: ignore
import itertools as it #type: ignore
from itertools import permutations #type: ignore
from itertools import combinations #type: ignore
from scipy.stats import zscore #type: ignore
import scipy.stats as st #type: ignore
import numpy as np #type: ignore
from . read import ReadData

class Probability:

    def cond_prob(self):

        # df movie
        df_movie = ReadData.movierating(self)

        # simple EDA
        print(df_movie.head())
        print("------")

        # find any null value
        print(df_movie.isnull().any())
        print("------")

        # find information for all columns
        print("General info:\n", df_movie.info())
        print("------")


        # print descriptive statistics of the data
        print("Descriptive statistics:\n", df_movie['rating'].describe())
        print("Descriptive statistics:\n", df_movie.describe(include = ['object']))
        print("------")

        # print additional descriptive statistics
        print("Median:\n", df_movie['rating'].median())
        print("------")

        print("Mode:\n", df_movie['rating'].mode())
        print("------")

        print("Skewness:\n", df_movie['rating'].skew())
        print("------")
        
        # probability of B (prior event)
        p_b = df_movie.groupby('rating').size().div(len(df_movie))


        # probability of A and B occured
        p_anb   = df_movie.groupby(['year','rating']).size().div(len(df_movie)).div(
                                            p_b,
                                            axis=0,
                                            level='rating'
        )

        # check the object type
        print(type(p_anb))
        print("------")

        # series to dataframe
        dataframeprob   = p_anb.to_frame().reset_index()

        # rename column
        dataframeprob.rename(columns={0: 'prob_score'}, inplace=True)

        print(dataframeprob)
        print(type(dataframeprob))