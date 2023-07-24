
import sys
import pandas as pd
import numpy as np 

from backorder.logger import logging
from backorder.exception import CustomException
from backorder.entity import artifacts_entity

from sklearn.preprocessing import LabelEncoder, OneHotEncoder, MinMaxScaler
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer

from sklearn.decomposition import PCA

from backorder.utils import save_array, save_object

from backorder.entity.config_entity import DataTransformationConfig



class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()

    def get_data_transformed(self):
        try:
            logging.info("dividing numerical and categorical features")
            numerical_features = ['national_inv', 'lead_time', 'in_transit_qty', 'forecast_3_month', 
                                'forecast_6_month', 'forecast_9_month', 'sales_1_month', 'sales_3_month',
                                'sales_6_month', 'sales_9_month', 'min_bank', 'pieces_past_due', 
                                'perf_6_month_avg', 'perf_12_month_avg', 'local_bo_qty']

            categorical_features = ['potential_issue', 'deck_risk', 'oe_constraint', 'ppap_risk', 
                                    'stop_auto_buy', 'rev_stop']

            logging.info("creating a pipeline")
            num_pipeline = Pipeline(
            steps=[
                ('imputer', SimpleImputer(strategy='median')),
                ('scaler', MinMaxScaler())
                ])

            cat_pipeline = Pipeline(
            steps=[
                ('ohe', OneHotEncoder())
                ])
            
            logging.info(f"Categorical columns: {categorical_features}")
            logging.info(f"Numerical columns: {numerical_features}")

            preprocessor = ColumnTransformer([
                ('num_pipeline', num_pipeline, numerical_features),
                ('cat_pipeline', cat_pipeline, categorical_features)
                ])
            logging.info("data transformation is completed")
            return preprocessor
        
        except Exception as e:
            raise CustomException(e, sys)    
        
        
    def initiate_data_transformation(self, train_path, test_path):
        try:

            logging.info("reading train and test data")
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)

            logging.info("Obtaining preprocessing object")
            preproccessor_obj = self.get_data_transformed()

            target_column = "went_on_backorder"


            logging.info("splitting train and test data into dependent variable and independent variables")
            input_feature_train_df = train_df.drop(columns=[target_column], axis=1)
            target_feature_train_df = train_df[target_column]

            input_feature_test_df = test_df.drop(columns=[target_column], axis=1)
            target_feature_test_df = test_df[target_column]
            
            logging.info("transformation on target columns")
            encoder = LabelEncoder()

            target_feature_train_arr = encoder.fit_transform(target_feature_train_df)
            target_feature_test_arr = encoder.transform(target_feature_test_df)

            logging.info(f"Applying preprocessing object on training data frame and testing data frame.")
            input_feature_train_arr = preproccessor_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr = preproccessor_obj.transform(input_feature_test_df)
            

            pca = PCA(n_components=0.95)
            X_train_pca = pca.fit_transform(input_feature_train_arr)
            X_test_pca = pca.transform(input_feature_test_arr)
            

            train_array = np.c_[X_train_pca, target_feature_train_arr]
            test_array = np.c_[X_test_pca, target_feature_test_arr]
            
            logging.info("saving preprocessing object")
            save_object(
                file_path = self.data_transformation_config.preprocessor_file_path,
                obj = preproccessor_obj
                )
            
            logging.info("saving array")
            save_array(self.data_transformation_config.train_array_path, train_array)
            save_array(self.data_transformation_config.test_array_path, test_array)

            
            return artifacts_entity.DataTransformationArtifacts(
                self.data_transformation_config.preprocessor_file_path,
                self.data_transformation_config.train_array_path,
                self.data_transformation_config.test_array_path
            )

        except Exception as e:
            raise CustomException(e, sys)