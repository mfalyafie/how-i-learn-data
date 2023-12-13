import math
import os, re, string
import os.path
import pickle
import pandas as pd #type: ignore
import numpy as np
from datetime import datetime as dt
from sklearn.model_selection import train_test_split #type: ignore
from sklearn.preprocessing import LabelEncoder, OneHotEncoder, StandardScaler #type: ignore
from sklearn.metrics import classification_report #type: ignore
from sklearn.compose import ColumnTransformer #type: ignore
from xgboost import XGBClassifier #type: ignore
from sklearn.neighbors import KNeighborsClassifier #type: ignore


class TrainingData:

    def train(self):
        
        print(os.getcwd())
        # read data
        df_bank = pd.read_csv("./application/data/train/train.csv", sep = ";")
        

        # Remove it since it is irrelevant for the model
        df_bank_clean = df_bank.drop(['day', 'month'], axis = 1).copy().reset_index(drop = True)

        # check all the features after removal
        print("General info:") 
        print(df_bank_clean.info())
        print('=========================================')

        # define X and y
        X = df_bank_clean.iloc[:, :-1].values
        y = df_bank_clean.iloc[:, -1].values
        print('X:\n', X)
        print('=========================================')
        print('y:\n', y)
        print('=========================================')

        # Categorical data encoding (onehot for independent, label for dependenet)
        le = LabelEncoder() # for dependent variable
        y_train = le.fit_transform(y)

        X_obj = []
        for i in range(len(X[0])):
            if np.array(df_bank_clean.drop('y', axis = 1).dtypes)[i] != 'O':
                continue
            X_obj.append(i)
        
        print('Columns with object data type:\n', X_obj)
        print('=========================================')

        ct1 = ColumnTransformer(transformers=[('encoder', OneHotEncoder(drop='first'), X_obj)], 
        remainder= 'passthrough') # for independent variables (dummy encoding to avoid dummy variable trap)

        ct2 = ColumnTransformer([('scaler', StandardScaler(), [-1, -2, -3, -4, -5, -6])], 
        remainder= 'passthrough')

        xg = XGBClassifier(random_state = 0)

        X_train = ct1.fit_transform(X)
        print('Example of X_train rows after encoding:\n', X_train[0])

        X_train = ct2.fit_transform(X_train)
        print('Example of X_train rows after scaling:\n', X_train[0])

        xg.fit(X_train, y_train)

        # model name as datetime
        model_name = dt.now().strftime('%Y%m%d%H%M%S%f')

        # create absolute path classfier naive bayes
        model_clf = './application/model/clf/{}.clf'.format(model_name)

        # absolute path encoder
        model_encoder = './application/model/encoder/{}.clf'.format(model_name)

        # absolute path scaler
        model_scaler = './application/model/scaler/{}.clf'.format(model_name)

        if model_clf is not None:
            with open(model_clf, 'wb') as f:
                pickle.dump(xg, f)

        if model_clf is not None:
            with open(model_encoder, 'wb') as f:
                pickle.dump(ct1, f)
        
        if model_clf is not None:
            with open(model_scaler, 'wb') as f:
                pickle.dump(ct2, f)