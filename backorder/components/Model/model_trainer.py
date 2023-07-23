import sys

from backorder.logger import logging
from backorder.exception import CustomException
from backorder.entity.artifacts_entity import DataTransformationArtifacts

from backorder.utils import save_object, load_array, evaluate_model

from backorder.entity.config_entity import ModelTrainerConfig

from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, classification_report

class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()

    def initiate_model_trainer(self, data_transformation_artifacts:DataTransformationArtifacts):
        try:
            logging.info("initiate model training")
            train_arr = load_array(file=data_transformation_artifacts.train_array_path)
            test_arr = load_array(file=data_transformation_artifacts.test_array_path)

            logging.info("splitting train and test array into independent and dependent variables")
            X_train, y_train, X_test, y_test = (
                                                train_arr[:,:-1], train_arr[:,-1],
                                                test_arr[:,:-1], test_arr[:,-1]
                                                )
            logging.info("defining various classification models")
            models = {
                "LogisticRegression": LogisticRegression(max_iter=1000),
                "DecisionTreeClassifier": DecisionTreeClassifier(max_depth=10)
            }

            model_report:dict = evaluate_model(X_train=X_train, y_train=y_train, X_test=X_test, y_test=y_test, models = models)
            
            logging.info("to get best model score from dict")
            best_score = max(sorted(model_report.values()))
            logging.info(f"best_score: {best_score}")

            logging.info("to get best model name from dict")
            best_model_name = list(model_report.keys())[
                list(model_report.values()).index(best_score)
            ]
            logging.info(f"best_model_name: {best_model_name}")
            
            best_model = models[best_model_name]
            logging.info(f"best model: {best_model}")

            if best_score < 0.6:
                raise CustomException("No best model is found", sys)
            logging.info(f"best model found on dataset")

            logging.info("saving model.pkl file")
            save_object(file_path=self.model_trainer_config.model_file_path,
                        obj=best_model)
            
            y_pred = best_model.predict(X_test)
            accuracy = accuracy_score(y_test, y_pred)
            classificationReport = classification_report(y_test, y_pred)

            logging.info("model training completed")
            return accuracy

        except Exception as e:
            raise CustomException(e, sys)    


    