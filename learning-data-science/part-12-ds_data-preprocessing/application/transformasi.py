"""
    m.fauzanalyafie@gmail.com
    24-Agustus-2022 17:58 PM
"""

import numpy as np #type: ignore
import pandas as pd #type: ignore
import seaborn as sns #type: ignore
from pandas_profiling import ProfileReport #type: ignore
import matplotlib.pyplot as plt #type:ignore
from sklearn.impute import SimpleImputer #type: ignore
from .read import Read

class Transformation:

    def cars(self):

        # df movie
        df_cars = Read.cars_csv(self)

        # simple EDA
        print(df_cars.head())
        print("------")
        
        # removing any symbol on price column
        disallowed_characters = ",._!$"
        for character in disallowed_characters:
            df_cars['Price'] = df_cars['Price'].str.replace(character, "")
        
        # replace not priced value to nan, allowing the column to be integer
        df_cars['Price'] = df_cars['Price'].replace("Not Priced", np.nan)
        
        # test if it's possible to change price to integer
        df_cars['Price'] = pd.to_numeric(df_cars['Price'])

        # change '[car manufacturer] certified' to 'certified' in New/Used column
        for i in range(len(df_cars)):
            if 'Certified' in df_cars['Used/New'][i]:
                df_cars['Used/New'][i] = 'Certified'

        # change '-' value in every column with object data type
        df_cars.replace('–', np.nan, inplace = True)

        # change year to become an object column
        df_cars['Year'] = df_cars['Year'].astype('object')

        # check if everything is pre-processed correctly from the general info (should have some nan values)
        df_cars.info()
        print("------")

        # replace all nan values with median of the respective column
        numeric_column = df_cars.select_dtypes(include = np.number).columns
        imputer = SimpleImputer(missing_values=np.nan, strategy="median")
        imputer.fit(df_cars[numeric_column])
        df_cars[numeric_column] = imputer.transform(df_cars[numeric_column])

        # check if there's still any null value left
        print(df_cars.isnull().any())
        print("------")

        # find information for all columns
        print("General info:\n", df_cars.info())
        print("------")


        # print descriptive statistics of the data
        print("Descriptive statistics:\n", df_cars.describe(include = [np.number]).T)
        print("------")
        print("Descriptive statistics:\n", df_cars.describe(include = ['object']).T)
        print("------")

        # print additional descriptive statistics
        print("Median:\n", df_cars.median(numeric_only = True))
        print("------")

        print("Mode:\n", df_cars.mode(numeric_only = True).T)
        print("------")

        print("Skewness:\n", df_cars.skew(numeric_only = True))
        print("------")
        
        # -------------------------------------create EDA plot------------------------------------------------
        
        # set color
        sns.set_style("darkgrid")

        try:
            
            num = df_cars.select_dtypes(include=np.number)  # Get numeric columns
            n = num.shape[1]  # Number of cols

            fig, axes = plt.subplots(n, 1, figsize=(5, 100))  # create subplots

            for ax, col in zip(axes, num):  # For each column...
                sns.distplot(num[col], ax=ax)   # Plot histogaerm
                ax.set_title(str(col)) # create title for each subplot

            # save dist plot
            plt.savefig("./chart/distplot_numeric_column.png")

            # clear current fig
            plt.cla()

            # print status
            print("success save image")

        except:

            print("cannot save image")

        try:

            fig, axs = plt.subplots(1, 1, figsize=(20, 20))
            df_cars['Used/New'].value_counts().plot(kind='pie', autopct='%.2f', 
            title = 'Used/New Cars Distribution', ax = axs) # create pie chart
            
            # save pie chart sub plot
            plt.savefig("./chart/used_new_car_distribution.png")

            # clear current fig
            plt.cla()

            # print status
            print("success save image")
        
        except:
            print('cannot save image')

        try:

            fig, axs = plt.subplots(1, 1, figsize=(40, 20))

            # box plot
            sns.boxplot(x = 'Make', y = 'Price', data= df_cars, ax = axs)

            # save box plot
            plt.savefig("./chart/boxplot_made_price.png")

            # clear current fig
            plt.cla()

            # print status
            print("success save image")
        
        except:

            print('cannot save image')

        try:

            # profiling dataset
            profile_data_cars = ProfileReport(df_cars, title="Cars Profiling")

            # save data
            profile_data_cars.to_file("./profiling/cars_profiling.html")

            print("success save profiling")

        except:

            print("cannot save")
        # ------------------ Conditional Probability -------------------------------

        # probability of B (prior event)
        p_b = df_cars.groupby('SellerType').size().div(len(df_cars))


        # probability of A if B occured
        p_a_when_b   = df_cars.groupby(['ComfortRating','SellerType']).size().div(len(df_cars)).div(
                                            p_b,
                                            axis=0,
                                            level='SellerType'
        )

        # check the object type
        print(type(p_a_when_b))
        print("------")

        # series to dataframe
        dataframeprob   = p_a_when_b.to_frame().reset_index()

        # rename column
        dataframeprob.rename(columns={0: 'prob_score'}, inplace=True)

        print(dataframeprob)
        print(type(dataframeprob))