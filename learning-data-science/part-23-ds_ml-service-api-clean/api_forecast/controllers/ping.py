""""
    author
"""

from fastapi import APIRouter #type: ignore
from datetime import datetime as dt
import os, numpy as np, pandas as pd #type: ignore
import pickle, json

router: APIRouter = APIRouter()

def load_model(model_path):
    with open(model_path, 'rb') as f:
        return pickle.load(f)

@router.get("/get-data")
def ping():
    return {"msg": "success"}

@router.get("/get-latest-ml-model")
def model_ml():


    ModelDir = './api_forecast/model/clf/{}.clf'

    try:
        models = [
            dt.strptime(model.replace('.clf', ''), '%Y%m%d%H%M%S%f')
            for model in os.listdir("./api_forecast/model/clf/")
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
    
    return {"json_data": model_path}

@router.post("/term-deposit-prediction")
def term_deposit_prediction(age: int, job: str, marital: str, education: str, default: str, balance: int, housing: str,
 loan: str, contact: str, duration: int, campaign: int, pdays: int, previous: int, poutcome: str):

    # klasifikasi model : clf = klasifikasi
    path            = "./api_forecast/model/clf/20221019183954469374.clf"
    
    # encoder model
    path1           = "./api_forecast/model/encoder/20221019183954469374.clf"

    # scaler model
    path2           = "./api_forecast/model/scaler/20221019183954469374.clf"

    model_clf       =  load_model(path)

    model_encoder    =  load_model(path1)

    model_scaler    =  load_model(path2)
    
    yage = int(age)
    yjob = job
    ymarital = marital
    yeducation = education
    ydefault = default
    ybalance = int(balance)
    yhousing = housing
    yloan = loan
    ycontact = contact
    yduration = int(duration)
    ycampaign = int(campaign)
    ypdays = int(pdays)
    yprevious = int(previous)
    ypoutcome = poutcome
    
    y_test = np.array([yage, yjob, ymarital, yeducation, ydefault, ybalance, yhousing, yloan,
    ycontact, yduration, ycampaign, ypdays, yprevious, ypoutcome]).reshape(1, -1)

    c1_data = model_encoder.transform(y_test)
    c2_data = model_scaler.transform(c1_data)
    c2_data = np.array(c2_data, dtype = float)

    y_preds = model_clf.predict(c2_data)


    #dengan asumsi bahwa 1 merupakan label positif
    if y_preds == 1:
        
        details = {
                    'Result' : 'Positive'
                }
        predict = pd.DataFrame(details, index = ['1'])

        out_var = predict.to_json(orient='records')

        datajsonreturn = json.loads(out_var)

    else:
        
        details = {
                    'Result' : 'Negative'
                }
        predict = pd.DataFrame(details, index = ['1'])

        out_var = predict.to_json(orient='records')

        datajsonreturn = json.loads(out_var)
    
    return {"msg": datajsonreturn}