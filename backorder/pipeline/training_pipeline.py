
from backorder.components.Data.data_ingestion import DataIngestion
from backorder.components.Data.data_transformation import DataTransformation
from backorder.components.Data.data_validation import DataValidation

from backorder.components.Model.model_trainer import ModelTrainer
from backorder.entity.artifacts_entity import DataIngestionArtifacts
from backorder.entity.config_entity import DataValidationConfig

class TrainingPipeline:

    data_ingestion = DataIngestion().initiate_data_ingestion()

    data_validation_config = DataValidationConfig()
    data_validation = DataValidation()
        
    data_validation = data_validation.initiate_data_validation()



    data_transformation = DataTransformation().initiate_data_transformation(
            train_path=data_ingestion.train_data_path,
            test_path = data_ingestion.test_data_path
        )
    model_trainer = ModelTrainer().initiate_model_trainer(data_transformation)

