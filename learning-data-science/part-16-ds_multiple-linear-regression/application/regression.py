"""
    m.fauzanalyafie@gmail.com
    4-September-2022 02:56
"""

import pandas as pd #type: ignore
import matplotlib.pyplot as plt #type: ignore
from sklearn.model_selection import train_test_split #type: ignore
from sklearn.linear_model import LinearRegression #type: ignore
from sklearn import metrics #type: ignore
import numpy as np #type: ignore
import seaborn as sns #type: ignore

class Regression:
    
    def __init__(self, csv_file):
    
        # initiate a parameter for the csv file to be inputted
        self.csv_file = csv_file

    def simple_linear(self):

        # input and change the csv file into a dataframe
        df_sl = pd.read_csv("{}".format(self.csv_file))

        # check all the features
        df_sl.info()

        # filter only for numeric columns
        numeric_value = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']
        df_sl_num = df_sl.select_dtypes(include=numeric_value)

        # create a distplot for every numeric column
        try:
            
            num = df_sl_num  # Get numeric columns
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
        
        # create a correlation heatmap for every numeric column
        try:
        
            # Increase the size of the heatmap.
            plt.figure(figsize=(16, 6))
            # Store heatmap object in a variable to easily access it when you want to include more features (such as title).
            # Set the range of values to be displayed on the colormap from -1 to 1, and set the annotation to True to display the correlation values on the heatmap.
            heatmap = sns.heatmap(df_sl_num.corr(), vmin=-1, vmax=1, annot=True)
            # Give a title to the heatmap. Pad defines the distance of the title from the top of the heatmap.
            heatmap.set_title('Correlation Heatmap', fontdict={'fontsize':12}, pad=12)

            # save box plot
            plt.savefig("./chart/corr_matrix.png")

            # clear current fig
            plt.cla()

            # print status
            print("success save image")
            print('=======================')

        except:

            print('cannot save image')
            print('=======================')

        # define the variable x and y
        X = df_sl_num.iloc[:, :-1].values
        y = df_sl_num.iloc[:, -1].values 

        # select and fit the model
        try:

            df_sl_col = df_sl.select_dtypes(include=numeric_value).columns
            results = []
            n = len(X[0])
            n_range = range(n)
            fig, ax = plt.subplots(n, figsize=(10, 30))
            for i in n_range:  # For each column...
                X_train, X_test, y_train, y_test = train_test_split(
                    X[:, i].reshape(-1, 1), y.reshape(-1, 1), test_size = 0.2, random_state = 42
                    )
                lm_reg = LinearRegression()
                lm_reg.fit(X_train, y_train)
                coef = lm_reg.coef_
                intercept = lm_reg.intercept_
                r_square = lm_reg.score(X_test, y_test)
                results.append({
                    'Feature (X)': str(df_sl_col[i]),
                    'Coefficient': coef,
                    'Intercept': intercept,
                    'R Square Score': r_square
                })
                # create scatter plot with regression line
                y_pred = lm_reg.predict(X_test)
                ax[i].scatter(X_test, y_test)
                ax[i].plot(X_test, y_pred, c='r')
                ax[i].set_title(str(df_sl_col[i]))
            
            plt.savefig("./chart/scatterplot_trendline.png")
            
            plt.cla()

            print('success save image')
            print('=======================')
        
        except:

            print('cannot save image')
            print('=======================')

        # print result (intercept, coefficient, r score, p value)
        df_results = pd.DataFrame(results)
        print('Simple linear regression results\n', df_results)
        print('=======================')
    
    def multiple_linear(self):

        # input and change the csv file into a dataframe
        df_sl = pd.read_csv("{}".format(self.csv_file))

        # check all the features
        df_sl.info()

        # filter only for numeric columns
        numeric_value = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']
        df_sl_num = df_sl.select_dtypes(include=numeric_value)
        
        # create a distplot for every numeric column
        try:
            
            num = df_sl_num  # Get numeric columns
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
            print('=======================')

        except:

            print("cannot save image")
            print('=======================')
        
        # create a correlation heatmap for every numeric column
        try:
        
            # Increase the size of the heatmap.
            plt.figure(figsize=(16, 6))
            # Store heatmap object in a variable to easily access it when you want to include more features (such as title).
            # Set the range of values to be displayed on the colormap from -1 to 1, and set the annotation to True to display the correlation values on the heatmap.
            heatmap = sns.heatmap(df_sl_num.corr(), vmin=-1, vmax=1, annot=True)
            # Give a title to the heatmap. Pad defines the distance of the title from the top of the heatmap.
            heatmap.set_title('Correlation Heatmap', fontdict={'fontsize':12}, pad=12)

            # save box plot
            plt.savefig("./chart/corr_matrix.png")

            # clear current fig
            plt.cla()

            # print status
            print("success save image")
            print('=======================')

        except:

            print('cannot save image')
            print('=======================')

        # define the variable x and y
        X = df_sl_num.iloc[:, :-1].values
        y = df_sl_num.iloc[:, -1].values

        # split the data into training and test set
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 42)

        # select and fit the model
        lm_reg = LinearRegression()
        lm_reg.fit(X_train, y_train)

        print('Coefficients:\n', lm_reg.coef_)
        print('=======================')
        print('Intercept:\n', lm_reg.intercept_)
        print('=======================')
        print('R Square Score:\n', lm_reg.score(X_test, y_test))
        print('=======================')

        # predict test set and show the differences
        preddata = lm_reg.predict(X_test)
        df_pred = pd.DataFrame({"real_data": y_test, "pred": preddata})
        print('Example of predicted data:\n', df_pred.head())
        print('=======================')

        # review the performance of the model based on test set
        print('MAE:', metrics.mean_absolute_error(y_test, preddata))
        print('MSE:', metrics.mean_squared_error(y_test, preddata))
        print('RMSE:', np.sqrt(metrics.mean_squared_error(y_test, preddata)))