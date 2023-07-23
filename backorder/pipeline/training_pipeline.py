
from backorder.components.Data.data_ingestion import DataIngestion
from backorder.components.Data.data_transformation import DataTransformation

from backorder.components.Model.model_trainer import ModelTrainer




def initiate_training_pipeline(self):

    data_ingestion = DataIngestion().initiate_data_ingestion()
    data_transformation = DataTransformation().initiate_data_transformation(
            train_path=data_ingestion.train_data_path,
            test_path = data_ingestion.test_data_path
        )
    model_trainer = ModelTrainer().initiate_model_trainer(data_transformation)

