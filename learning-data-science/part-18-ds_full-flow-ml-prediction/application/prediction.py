# Import necessary libraries
import pandas as pd #type: ignore
import matplotlib.pyplot as plt #type: ignore
from sklearn.model_selection import train_test_split #type: ignore
from sklearn.linear_model import LinearRegression #type: ignore
from sklearn import metrics #type: ignore
import numpy as np #type: ignore
import seaborn as sns #type: ignore
from sklearn.tree import DecisionTreeClassifier #type: ignore
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, f1_score #type: ignore
from pandas_profiling import ProfileReport #type: ignore

class Prediction:

    # Initiate paramters for csv_file and independent variable cutoff (not included in the model)
    def __init__(self, csv_file, var_cutoff):
        
        self.csv_file = csv_file
        self.var_cutoff = var_cutoff
    
    def multiple_linear(self):

        # input and change the csv file into a dataframe
        df_heart = pd.read_csv("{}".format(self.csv_file))

        # --------------------- Descriptive Analytics ----------------------
        
        # check all the features
        print("General info:") 
        print(df_heart.info())
        print("------")

        # check if there's still any null value left
        print('Is there any null in each column left?')
        print(df_heart.isnull().any())
        print("------")
        
        # print descriptive statistics of the data
        print("Descriptive statistics:")
        print(df_heart.describe())
        print("------")
        
        # print additional descriptive statistics
        print("Median:\n", df_heart.median(numeric_only = True))
        print("------")

        print("Mode:\n", df_heart.mode(numeric_only = True))
        print("------")

        print("Skewness:\n", df_heart.skew(numeric_only = True))
        print("------")

        # --------------------- EDA Plot ----------------------
        
        # filter only for numeric columns
        numeric_value = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']
        df_heart_num = df_heart.select_dtypes(include=numeric_value)

        # create a distplot for every numeric column
        try:
            
            num = df_heart_num  # Get numeric columns
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
            heatmap = sns.heatmap(df_heart_num.corr(), vmin=-1, vmax=1, annot=True)
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

        try:

            # profiling dataset
            profile_data_heart = ProfileReport(df_heart, title="heart Profiling")

            # save data
            profile_data_heart.to_file("./profiling/heart_profiling.html")

            print("success save profiling")
            print('=======================')

        except:

            print("cannot save")
            print('=======================')
        
        # --------------------- MLR Model ----------------------
        
        # define the variable x and y
        X = df_heart_num.iloc[:, self.var_cutoff:-1].values
        y = df_heart_num.iloc[:, -1].values

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
        print('=========================================')
        print('MSE:', metrics.mean_squared_error(y_test, preddata))
        print('=========================================')
        print('RMSE:', np.sqrt(metrics.mean_squared_error(y_test, preddata)))
        print('=========================================')

    def decision_tree_classification(self):

        # input and change the csv file into a dataframe
        df_heart = pd.read_csv("{}".format(self.csv_file))

        # --------------------- Descriptive Analytics ----------------------
        
        # check all the features
        print("General info:") 
        print(df_heart.info())
        print("------")

        # check if there's still any null value left
        print('Is there any null in each column left?')
        print(df_heart.isnull().any())
        print("------")
        
        # print descriptive statistics of the data
        print("Descriptive statistics:")
        print(df_heart.describe())
        print("------")
        
        # print additional descriptive statistics
        print("Median:\n", df_heart.median(numeric_only = True))
        print("------")

        print("Mode:\n", df_heart.mode(numeric_only = True))
        print("------")

        print("Skewness:\n", df_heart.skew(numeric_only = True))
        print("------")

        # --------------------- EDA Plot ----------------------
        
        # filter only for numeric columns
        numeric_value = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']
        df_heart_num = df_heart.select_dtypes(include=numeric_value)

        # create a distplot for every numeric column
        try:
            
            num = df_heart_num  # Get numeric columns
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
            heatmap = sns.heatmap(df_heart_num.corr(), vmin=-1, vmax=1, annot=True)
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

        try:

            # profiling dataset
            profile_data_heart = ProfileReport(df_heart, title="heart Profiling")

            # save data
            profile_data_heart.to_file("./profiling/heart_profiling.html")

            print("success save profiling")
            print('=======================')

        except:

            print("cannot save")
            print('=======================')
        
        # feature selection
        X = df_heart.iloc[:, self.var_cutoff:-1].values
        y = df_heart.iloc[:, -1].values

        # Split the training and test set
        X_train, X_test, y_train, y_test =  train_test_split(X, y, test_size=0.2, random_state=42)

        # Train the model based on X train and y train
        classifier = DecisionTreeClassifier(criterion = "entropy", random_state=42)
        classifier.fit(X_train, y_train)

        # Predict the test set based on model
        y_pred = classifier.predict(X_test)
        print(np.concatenate((y_pred.reshape(len(y_pred), 1), y_test.reshape(len(y_test), 1)), 1))
        print('=======================')

        # Evaluate the performance with important metrics
        cm = confusion_matrix(y_test, y_pred)
        acc = accuracy_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)

        # Check all the important metrics created
        print('Confusion Matrix:\n', cm)
        print('=========================================')
        print('Accuracy Score:\n', acc)
        print('=========================================')
        print('F1 Score:\n', f1)
        print('=========================================')