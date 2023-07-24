import sys
from backorder.logger import logging
from backorder.exception import CustomException

import pandas as pd
import numpy as np

from sklearn.metrics import accuracy_score
from sklearn.compose import ColumnTransformer

from backorder.entity.artifacts_entity import DataIngestionArtifacts, DataTransformationArtifacts, ModelTrainerArtifacts

from backorder import utils

class ModelEvaluation:
    def __init__(self,
                model_trainer_artifacts: ModelTrainerArtifacts,
                data_transformation_artifacts: DataTransformationArtifacts,
                data_ingestion_artifacts: DataIngestionArtifacts):
        
        self.data_ingestion_artifacts = data_ingestion_artifacts
        self.data_transformation_artifacts = data_transformation_artifacts
        self.model_trainer_artifacts = model_trainer_artifacts

    def load_stored_objects(self, model_path, transform_path):    
        try:
            model = utils.load_object(model_path)
            transform = utils.load_object(transform_path)
            return model, transform    

        except Exception as e:
            raise CustomException(e, sys)    
        
    def initiate_model_evaluate(self):
        try:
            pass
        except Exception as e:
            raise CustomException(e, sys)    