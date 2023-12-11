"""
    m.fauzanalyafie@gmail.com
    31-Agustus-2022 13:58
"""

# import necessary libraries
import numpy as np #type: ignore
import pandas as pd #type: ignore
import seaborn as sns #type: ignore
from pandas_profiling import ProfileReport #type: ignore
import matplotlib.pyplot as plt #type:ignore
from sklearn.impute import SimpleImputer #type: ignore
from .read import Read

class Eda:

    def stock(self):

        # df movie
        df_stock = Read.stock_market(self)

        # ---------------------------- Data Preprocessing ----------------------
        
        # see what kind of data it is like
        print(df_stock.head())
        print("------")

        # check the data type if there's any column with a wrong one
        print("General info:\n", df_stock.info())
        print("------")
        
        # change the date into a datetime/timestamp data type
        df_stock['Date'] = pd.to_datetime(df_stock['Date'])

        # Div Yield % is still object, there might be null values that are considered as string
        def unique(list1):
  
            # initialize a null list
            unique_list = []
        
            # traverse for all elements
            for x in list1:
                # check if exists in unique_list or not
                if x not in unique_list:
                    unique_list.append(x)
            # print list
            return sorted(unique_list)

        # call the function to show unique values, looking at the possible null values
        unique(df_stock['Div Yield %'])

        # '-' is the supposed-to-be null value, so let's change it to NaN
        df_stock = df_stock.replace('-', np.nan)

        # fill the NaN with median value
        df_stock["Div Yield %"].fillna(df_stock["Div Yield %"].median(), inplace=True)

        # change div yield to numeric
        df_stock["Div Yield %"] = pd.to_numeric(df_stock["Div Yield %"])

        # --------------------- Descriptive Analytics ----------------------
        
        # check if data type has changed
        print("General info:") 
        print(df_stock.info())
        print("------")

        # check if there's still any null value left
        print('Is there any null in each column left?')
        print(df_stock.isnull().any())
        print("------")
        
        # print descriptive statistics of the data
        print("Descriptive statistics:")
        print(df_stock.describe())
        print("------")
        
        # print additional descriptive statistics
        print("Median:\n", df_stock.median(numeric_only = True))
        print("------")

        print("Mode:\n", df_stock.mode(numeric_only = True))
        print("------")

        print("Skewness:\n", df_stock.skew(numeric_only = True))
        print("------")
        
        # -------------------------------------create EDA plot------------------------------------------------
        
        # set color
        sns.set_style("darkgrid")

        try:
            
            num = df_stock.select_dtypes(include=np.number)  # Get numeric columns
            n = num.shape[1]  # Number of cols

            fig, axes = plt.subplots(n, 1, figsize=(10, 30))  # create subplots

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
            
            num = df_stock.select_dtypes(include=np.number)  # Get numeric columns
            n = num.shape[1]  # Number of cols

            fig, axes = plt.subplots(n, 1, figsize=(10, 30))  # create subplots

            for ax, col in zip(axes, num):  # For each column...
                sns.lineplot(data = df_stock, x="Date", y= col, ax = ax) # plot lineplot
                ax.set_title(str(col)) # create title for each subplot

            # save dist plot
            plt.savefig("./chart/lineplot_numeric_column.png")

            # clear current fig
            plt.cla()

            # print status
            print("success save image")

        except:

            print("cannot save image")

        try:
        
            # Increase the size of the heatmap.
            plt.figure(figsize=(16, 6))
            # Store heatmap object in a variable to easily access it when you want to include more features (such as title).
            # Set the range of values to be displayed on the colormap from -1 to 1, and set the annotation to True to display the correlation values on the heatmap.
            heatmap = sns.heatmap(df_stock.corr(), vmin=-1, vmax=1, annot=True)
            # Give a title to the heatmap. Pad defines the distance of the title from the top of the heatmap.
            heatmap.set_title('Correlation Heatmap', fontdict={'fontsize':12}, pad=12)

            # save box plot
            plt.savefig("./chart/corr_matrix.png")

            # clear current fig
            plt.cla()

            # print status
            print("success save image")

        except:

            print('cannot save image')

        try:

            # profiling dataset
            profile_data_cars = ProfileReport(df_stock, title="Cars Profiling")

            # save data
            profile_data_cars.to_file("./profiling/cars_profiling.html")

            print("success save profiling")

        except:

            print("cannot save")