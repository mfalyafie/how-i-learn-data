# Import necessary libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, f1_score
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.impute import SimpleImputer
from pandas_profiling import ProfileReport

# Create class for random forest model
class RandomForest:

    # Initiate parameters for csv file and var cutoff
    def __init__(self, csv_file, var_cutoff_left, var_cutoff_right):
        
        self.csv_file = csv_file
        self.var_cutoff_left = var_cutoff_left
        self.var_cutoff_right = var_cutoff_right
    
    # Create function for random forest classification
    def classification(self):

        # --------------------- Data Pre-processing 1 ----------------------

        # Read the data and check its contents
        df_churn = pd.read_excel(self.csv_file)
        print('First 5 rows of data:\n', df_churn.head())
        print('=========================================')

        df_churn = df_churn.replace(' ', np.nan)
        df_churn['Total Charges'] = pd.to_numeric(df_churn['Total Charges'])

        # --------------------- Descriptive Analytics ----------------------
        
        # check all the features
        print("General info:") 
        print(df_churn.info())
        print('=========================================')

        # check if there's still any null value left
        print('Is there any null in each column left?')
        print(df_churn.isnull().any())
        print('=========================================')
        
        # print descriptive statistics of the data
        print("Descriptive statistics:")
        print(df_churn.describe())
        print('=========================================')
        
        # print additional descriptive statistics
        print("Median:\n", df_churn.median(numeric_only = True))
        print('=========================================')

        print("Mode:\n", df_churn.mode(numeric_only = True))
        print('=========================================')

        print("Skewness:\n", df_churn.skew(numeric_only = True))
        print('=========================================')

        # --------------------- EDA Plot ----------------------
        
        # Filter only for numeric columns
        numeric_value = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']
        df_churn_num = df_churn.select_dtypes(include=numeric_value)

        # Create a distplot for every numeric column
        try:
            
            num = df_churn.select_dtypes(include = 'object')  # Get numeric columns
            n = num.shape[1]  # Number of cols

            fig, axes = plt.subplots(n, 1, figsize=(10, 100), constrained_layout = True)  # create subplots
            id_substring = 'id'

            for ax, col in zip(axes, num):  # For each column...

                if len(num[col].unique()) > 10:
                    continue

                sns.countplot(data = num, x = col, hue = 'Churn Label', ax=ax)   # Plot histogaerm
                ax.set_title(str(col)) # create title for each subplot

            # save plot
            plt.savefig("./chart/countplot_colummn_churn.png")

            # clear current fig
            plt.cla()

            # print status
            print("success save image")
            print('=========================================')

        except:

            print("cannot save image")
            print('=========================================')
        
        # Create a correlation heatmap for every numeric column
        try:
        
            # Increase the size of the heatmap.
            plt.figure(figsize=(16, 6))
            # Store heatmap object in a variable to easily access it when you want to include more features (such as title).
            # Set the range of values to be displayed on the colormap from -1 to 1, and set the annotation to True to display the correlation values on the heatmap.
            heatmap = sns.heatmap(df_churn_num.corr(), vmin=-1, vmax=1, annot=True)
            # Give a title to the heatmap. Pad defines the distance of the title from the top of the heatmap.
            heatmap.set_title('Correlation Heatmap', fontdict={'fontsize':12}, pad=12)

            # save plot
            plt.savefig("./chart/corr_matrix.png")

            # clear current fig
            plt.cla()

            # print status
            print("success save image")
            print('=========================================')

        except:

            print('cannot save image')
            print('=========================================')

        # Create a pie chart for dependent variable
        try:

            fig_data  = plt.figure()
            # add axes ([xmin, ymin, dx, dy])
            axes_data = fig_data.add_axes([0, 0, 1, 1])
            # add labels 
            churn_data  = df_churn['Churn Label'].value_counts()
            axes_data.pie(churn_data, labels = df_churn['Churn Label'].unique(), autopct='%.0f%%')

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

        # Create a profiling report
        try:

            # profiling dataset
            profile_data_churn = ProfileReport(df_churn, title="churn Profiling")

            # save data
            profile_data_churn.to_file("./profiling/churn_profiling.html")

            print("success save profiling")
            print('=========================================')

        except:

            print("cannot save")
            print('=========================================')
        
        # --------------------- Data Pre-processing 2 ----------------------

        # Create the correlation data frame
        df_churn_corr = df_churn.corr()
        df_churn_corr = df_churn_corr.replace(1, np.nan)
        
        # Check which columns have high correlations (>=|0.6|)
        print('Columns with high correlations:')
        for col in df_churn_corr:

            if df_churn_corr[col].max() >= abs(0.6):
                
                print(col)
        print('=========================================')

        # Remove columns with a potential of multicollinearity (highly correlated)
        for col in df_churn_corr:

            if df_churn_corr[col].max() >= abs(0.6):
                
                df_churn = df_churn.drop(columns = [col])
                df_churn_corr = df_churn_corr.drop(index = col, columns = col)
        
        print("General info after removing highly correlated columns:") 
        print(df_churn.info())
        print('=========================================')

        # Extract the features X and y
        X = df_churn.iloc[:, self.var_cutoff_left:self.var_cutoff_right].values
        y = df_churn.iloc[:, self.var_cutoff_right].values

        # Check the content of extracted features
        np.set_printoptions(suppress=True)
        print('Independent variables of the first row:\n', X[0])
        print('=========================================')
        print('Dependent variable:\n', y)
        print('=========================================')

        # Encode categorical variables
        le = LabelEncoder() # for dependent variable
        y = le.fit_transform(y)
        ct = ColumnTransformer(transformers=[('encoder', OneHotEncoder(drop='first'), list(range(16)))],
         remainder= 'passthrough') # for independent variables (dummy encoding to avoid dummy variable trap)
        X = np.array(ct.fit_transform(X))
        X = X.astype('float')
        y = y.astype('float')

        # Check the content after encoding process
        print('Independent variables of the first row:\n', X[0])
        print('=========================================')
        print('Dependent variable:\n', y)
        print('=========================================')

        # Check whether there is any null value in the array
        print('Location of the nan values in the array:\n', np.where(np.isnan(X)))
        
        # Change the nan values to the mean of the feature
        imputer = SimpleImputer(missing_values=np.nan, strategy="mean")
        imputer.fit(X)
        X = imputer.transform(X)

        # Check whether there is still any null value in the array
        print('Location of the nan values in the array:\n', np.where(np.isnan(X)))

        # Split between training and test set
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 42)

        # --------------------- Data Pre-processing 2 ----------------------

        # fitting model
        # n estimator default 10
        # entropy homogen
        rdf_model = RandomForestClassifier(n_estimators = 500, criterion='entropy')
        rdf_model.fit(X_train, y_train)

        # Predict the test set based on model
        y_pred = rdf_model.predict(X_test)

        # Evaluate the performance with important metrics
        cm = confusion_matrix(y_test, y_pred)
        acc = accuracy_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred, pos_label = 1)

        # Check all the important metrics created
        print('Confusion Matrix:\n', cm)
        print('=========================================')
        print('Accuracy Score:\n', acc)
        print('=========================================')
        print('F1 Score:\n', f1)
        print('=========================================')
        print('Classification Report:\n', classification_report(y_test, y_pred, target_names = ['Class 0', 'Class 1']))
        print('=========================================')
        
        



