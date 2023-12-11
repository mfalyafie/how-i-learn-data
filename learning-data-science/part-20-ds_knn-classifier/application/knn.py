# Import necessary libraries
import pandas as pd
import numpy as np
import sklearn
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report
from sklearn import metrics
import seaborn as sns
from sklearn.compose import ColumnTransformer
from pandas_profiling import ProfileReport

class KNN:

    # Initiate paramters for csv_file
    def __init__(self, csv_file, csv_file_test):

        self.csv_file = csv_file
        self.csv_file_test = csv_file_test
        

    # Create a function for KNN classfication
    def classification(self):

        # --------------------- Data Pre-processing 1 ----------------------
        
        # Read data and check its contents
        df_bank  =  pd.read_csv(self.csv_file, sep = ';')
        print('First 5 rows of data:\n', df_bank.head())
        print('=========================================')

        # check all the features
        print("General info:") 
        print(df_bank.info())
        print('=========================================')



        # check if there's still any null value left
        print('Is there any null in each column left?')
        print(df_bank.isnull().any())
        print('=========================================')

        # --------------------- Exploratory Data Analysis (EDA) ----------------------

        # print descriptive statistics of the data
        print("Descriptive statistics:")
        print(df_bank.describe())
        print('=========================================')
        
        # print additional descriptive statistics
        print("Median:\n", df_bank.median(numeric_only = True))
        print('=========================================')

        print("Mode:\n", df_bank.mode(numeric_only = True))
        print('=========================================')

        print("Skewness:\n", df_bank.skew(numeric_only = True))
        print('=========================================')

        # --------------------- EDA Plot ----------------------

        # filter only for numeric columns
        numeric_value = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']
        df_bank_num = df_bank.select_dtypes(include=numeric_value)
        
        # create a distplot for every numeric column
        try:
            
            num = df_bank_num  # Get numeric columns
            n = num.shape[1]  # Number of cols

            fig, axes = plt.subplots(n, 1, figsize=(10, 30))  # create subplots

            for ax, col in zip(axes, num):  # For each column...
                df_barplot = pd.concat(objs = [num[col], df_bank['y']], axis = 1, ignore_index = False)
                sns.barplot(data = df_barplot, x = 'y', y = col, ax=ax)   # Plot histogaerm
                ax.set_title(str(col)) # create title for each subplot

            print(df_barplot)

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
            heatmap = sns.heatmap(df_bank_num.corr(), vmin=-1, vmax=1, annot=True)
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
            profile_data_bank = ProfileReport(df_bank, title="Bank Profiling")

            # save data
            profile_data_bank.to_file("./profiling/bank_profiling.html")

            print("success save profiling")
            print('=======================')

        except:

            print("cannot save")
            print('=======================')
        
        # Create a distplot for categorical columns (with hue)
        try:

            col_df_bank = []
            for col in df_bank:
                if len(df_bank[col].unique()) > 31 or col == 'y':
                        continue
                col_df_bank.append(col)

            num = df_bank[col_df_bank]  # Get numeric columns

            n = num.shape[1]  # Number of cols

            fig, axes = plt.subplots(n, 1, figsize=(30, 100), constrained_layout = True)  # create subplots

            for ax, col in zip(axes, num):  # For each column...

                x,y = col, 'y'

                df1_bank = df_bank.groupby(x)['y'].value_counts(normalize=True).reset_index(name ='percent')

                sns.barplot(x=x,y='percent',hue='y',data=df1_bank, ax = ax)

            # save plot
            plt.savefig("./chart/distplot_category_column.png")

            # clear current fig
            plt.cla()

            # print status
            print("success save image")
            print('=======================')
            
        except:

            print('cannot save image')
            print('=======================')
        
        # Create a pie chart for dependent variable
        try:

            fig_data  = plt.figure()
            # add axes ([xmin, ymin, dx, dy])
            axes_data = fig_data.add_axes([0, 0, 1, 1])
            # add labels 
            bank_data  = df_bank['y'].value_counts()
            axes_data.pie(bank_data, labels = df_bank['y'].unique(), autopct='%.0f%%')

            # save plot
            plt.savefig("./chart/pie_chart_dependent.png")

            # clear current fig
            plt.cla()

            # print status
            print("success save image")
            print('=========================================')
        
        except:

            print('cannot save image')
            print('=========================================')

        # --------------------- Data Pre-processing 2 ----------------------

        # Remove it since it is irrelevant for the model
        df_bank_clean = df_bank.drop(['day', 'month'], axis = 1).copy().reset_index(drop = True)

        # check all the features after removal
        print("General info:") 
        print(df_bank_clean.info())
        print('=========================================')

        # --------------------- Data Modeling ----------------------

        # define X and y
        X = df_bank_clean.iloc[:, :-1].values
        y = df_bank_clean.iloc[:, -1].values
        print('X:\n', X)
        print('=========================================')
        print('y:\n', y)
        print('=========================================')

        # Read the test set file for testing model performance
        df_bank_test = pd.read_csv(self.csv_file_test, sep = ';')
        df_bank_test = df_bank_test.drop(['day', 'month'], axis = 1).copy().reset_index(drop = True)
        X_test = df_bank_test.iloc[:, :-1].values
        y_test = df_bank_test.iloc[:, -1].values

        # Categorical data encoding (onehot for independent, label for dependenet)
        le = LabelEncoder() # for dependent variable
        y_train = le.fit_transform(y)
        y_test = le.transform(y_test)
        print('y after label encoding:\n', y_train)
        print('y after label encoding:\n', y_test)
        print('=========================================')
        
        X_obj = []
        for i in range(len(X[0])):
            if np.array(df_bank_clean.drop('y', axis = 1).dtypes)[i] != 'O':
                continue
            X_obj.append(i)

        X_num = []
        for i in range(len(X[0])):
            if np.array(df_bank_clean.drop('y', axis = 1).dtypes)[i] == 'O':
                continue
            X_num.append(i)
        
        print('Columns with object data type:\n', X_obj)
        print('=========================================')

        print('Columns with numerical data type:\n', X_num)
        print('=========================================')
        
        ct = ColumnTransformer(transformers=[('encoder', OneHotEncoder(drop='first'), X_obj)], 
        remainder= 'passthrough') # for independent variables (dummy encoding to avoid dummy variable trap)
        X_train = ct.fit_transform(X)
        X_test = ct.transform(X_test)
        print('Example of X rows after encoding:\n', X_train[0])
        print('Example of X rows after encoding:\n', X_test[0])
        print('=========================================')

        # split data into training and test set
        #X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        #print('Jumlah baris dan kolom x_train:', X_train.shape, '----Jumlah barus dan kolom y_train adalah:', y_train.shape)
        #print('=========================================')

        from sklearn.preprocessing import StandardScaler
        ct2 = ColumnTransformer([('scaler', StandardScaler(), [-1, -2, -3, -4, -5, -6])], 
        remainder= 'passthrough')
        X_train = ct2.fit_transform(X_train)
        X_test = ct2.transform(X_test)
        #sc = StandardScaler()
        #X_train = sc.fit_transform(X_train)
        #X_test = sc.transform(X_test)

        print('Example of X_train rows after scaling:\n', X_train[0])
        print('=========================================')

        # Fitting the model to KNN classifier
        knn = KNeighborsClassifier(n_neighbors=3, metric='minkowski', p = 2)
        knn.fit(X_train, y_train)

        # Create classification report to measure model model performance
        y_pred = knn.predict(X_test)
        print('Classification Report')
        print(classification_report(y_test, y_pred))