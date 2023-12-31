from dataclasses import dataclass

@dataclass
class DataIngestionArtifacts:
    train_data_path:str
    test_data_path:str

@dataclass
class DataValidationArtifact:
    report_file_path:str    

@dataclass 
class DataTransformationArtifacts:
    preprocessor_file_path:str
    train_array_path:str
    test_array_path:str

@dataclass
class ModelTrainerArtifacts:
    model_file_path:str
    

@dataclass
class ModelEvaluationArtifacts:
    is_model_accepted: bool
    improved_accuracy: float       
