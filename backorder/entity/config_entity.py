from dataclasses import dataclass
import os

@dataclass
class DataIngestionConfig:
    raw_data_path:str = os.path.join("artifacts/Data_Ingestion", "raw.csv")
    train_data_path:str = os.path.join("artifacts/Data_Ingestion", "train.csv")
    test_data_path:str = os.path.join("artifacts/Data_Ingestion", "test.csv")

@dataclass
class DataTransformationConfig:
    preprocessor_file_path = os.path.join("artifacts/Data_Transformation", "preprocessor.pkl")    
    train_array_path = os.path.join("artifacts/Data_Transformation", "train_array.npy")
    test_array_path = os.path.join("artifacts/Data_Transformation", "test_array.npy")

@dataclass
class ModelTrainerConfig:
    model_file_path = os.path.join("artifacts/Model_Trainer", "model.pkl")