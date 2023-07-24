import os, sys
from backorder.exception import CustomException
import numpy as np
import dill
import yaml
from sklearn.metrics import accuracy_score
import pandas as pd

def convert_columns_float(df:pd.DataFrame,exclude_columns:list)->pd.DataFrame:
    try:
        for column in df.columns:
            if column not in exclude_columns:
                if df[column].dtypes != 'O':
                    df[column]=df[column].astype('float')
        return df
    except Exception as e:
        raise CustomException(e, sys)
    
def write_yaml_file(file_path,data:dict):
    try:
        os.makedirs(os.path.dirname(file_path),exist_ok=True)
        with open(file_path,"w") as file_writer:
            yaml.dump(data,file_writer)
    except Exception as e:
        raise CustomException(e, sys)    

def save_object(file_path, obj):
    try:
    
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'wb') as file_obj:
            dill.dump(obj, file_obj)

    except Exception as e:
        raise CustomException(e, sys)
    
def save_array(file, arr):

    os.makedirs(os.path.dirname(file), exist_ok=True)
    np.save(file, arr)

def load_array(file):

    return np.load(file)    

def evaluate_model(X_train, X_test, y_train, y_test, models):
    try:
        report = {}
        for i in range(len(list(models))):
            model = list(models.values())[i]
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)

            accuarcy = accuracy_score(y_test, y_pred)

            report[list(models.keys())[i]] = accuarcy

        return report

    except Exception as e:
        raise Exception(e, sys)


def load_object(file):
    try:
        with open(file, 'rb') as file_object:
            model = dill.load(file_object)
            return model

    except Exception as e:
        raise Exception(e, sys)

    