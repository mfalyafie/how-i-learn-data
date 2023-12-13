import pandas as pd #type: ignore
from sklearn.feature_extraction.text import TfidfVectorizer #type: ignore
from sklearn.naive_bayes import GaussianNB #type: ignore
from datetime import datetime as dt
import math, os, os.path, pickle, shutil
from . train import TrainingData

class ModelNotFound(Exception): pass

class ModelTrainer:
    

    def train(self):

        beg_dt = dt.now()

        self.mlmodel = TrainingData.train(self)
        
        print("Training completed in {} s".format(
            round((dt.now() - beg_dt).total_seconds(), 3)
        ))
