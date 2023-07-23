import os, sys
from backorder.exception import CustomException
import numpy as np
import dill

from sklearn.metrics import accuracy_score

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


# def load_object(file):
#     try:
#         with open(file, 'rb') as file_object:
#             model = dill.load(file_object)
#             return model

#     except Exception as e:
#         raise Exception(e, sys)

    