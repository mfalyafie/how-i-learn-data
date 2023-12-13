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


class TestData:


    def __init__(self, age, job, marital, education, default, balance, housing, loan, contact, duration, campaign, 
    pdays, previous, poutcome):

        self.age = age
        self.job = job
        self.marital = marital
        self.education = education
        self.default = default
        self.balance = balance
        self.housing = housing
        self.loan = loan
        self.contact = contact
        self.duration = duration
        self.campaign = campaign
        self.pdays = pdays
        self.previous = previous
        self.poutcome = poutcome

    @staticmethod
    def load_model(model_path):

        with open(model_path, 'rb') as f:

            return pickle.load(f)


    def test_data(self):

        ModelDir       = './application/model/clf/{}.clf'
        ModelDirEncoder = './application/model/encoder/{}.clf'
        ModelDirScaler = './application/model/scaler/{}.clf'

        try:
            models = [ 
                        dt.strptime(model.replace('.clf', ''), '%Y%m%d%H%M%S%f')

                        for model in os.listdir("./application/model/clf/")

                            if model.endswith('.clf')
            ]

        except:

            print("error")

        else:

            if not models:

                 print("model not found")

            else: 

                models.sort()

                model_path = ModelDir.format(

                    models[-1].strftime('%Y%m%d%H%M%S%f')
                )

                self.__model = self.load_model(model_path)

        
        try:
            models = [ 
                        dt.strptime(model.replace('.clf', ''), '%Y%m%d%H%M%S%f')

                        for model in os.listdir("./application/model/encoder/")

                            if model.endswith('.clf')
            ]

        except:

            print("error")
            
        else:

            if not models:

                 print("model not found")

            else: 

                models.sort()

                model_path = ModelDirEncoder.format(

                    models[-1].strftime('%Y%m%d%H%M%S%f')
                )

                self.__model_encoder = self.load_model(model_path)
        
        try:
            models = [ 
                        dt.strptime(model.replace('.clf', ''), '%Y%m%d%H%M%S%f')

                        for model in os.listdir("./application/model/scaler/")

                            if model.endswith('.clf')
            ]

        except:

            print("error")
            
        else:

            if not models:

                 print("model not found")

            else: 

                models.sort()

                model_path = ModelDirScaler.format(

                    models[-1].strftime('%Y%m%d%H%M%S%f')
                )

                self.__model_scaler = self.load_model(model_path)


        yage = int(self.age)
        yjob = self.job
        ymarital = self.marital
        yeducation = self.education
        ydefault = self.default
        ybalance = int(self.balance)
        yhousing = self.housing
        yloan = self.loan
        ycontact = self.contact
        yduration = int(self.duration)
        ycampaign = int(self.campaign)
        ypdays = int(self.pdays)
        yprevious = int(self.previous)
        ypoutcome = self.poutcome
        
        y_test = np.array([yage, yjob, ymarital, yeducation, ydefault, ybalance, yhousing, yloan,
        ycontact, yduration, ycampaign, ypdays, yprevious, ypoutcome]).reshape(1, -1)

        c1_data = self.__model_encoder.transform(y_test)

        c2_data = self.__model_scaler.transform(c1_data)
        c2_data = np.array(c2_data, dtype = float)

        y_preds = self.__model.predict(c2_data)


        #dengan asumsi bahwa 1 merupakan label positif
        if y_preds == 1:
            
            details = {
                        'Result' : 'Positive'
                    }
            predict = pd.DataFrame(details, index = ['1'])

            predict.to_json("abc_postives.json" ,orient='records', lines=True)

            print(predict)

            print('Positif')
        else:
            
            details = {
                        'Result' : 'Negative'
                    }
            predict = pd.DataFrame(details, index = ['1'])

            predict.to_json("abc_negative.json" ,orient='records', lines=True)

            print(predict)

            print('Negatif')