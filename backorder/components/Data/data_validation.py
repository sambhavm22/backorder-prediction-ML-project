from backorder.entity import config_entity
from backorder.entity import artifacts_entity
from backorder.logger import logging
from backorder.exception import CustomException

import os, sys
import pandas as pd
import numpy as np

from backorder.components.Data.data_ingestion import DataIngestion
from backorder.entity.artifacts_entity import DataIngestionArtifacts
from backorder.entity.config_entity import DataIngestionConfig

from backorder.entity.artifacts_entity import DataValidationArtifact
from backorder.entity.config_entity import DataValidationConfig

from backorder.utils import convert_columns_float, write_yaml_file


from scipy.stats import ks_2samp

TARGET_COLUMN = "went_on_backorder"

class DataValidation:
    
    def __init__(self):
        
        self.data_validation_config = DataValidationConfig()
        self.data_ingestion_artifact = DataIngestion()
        self.validation_error=dict()
    
    def dropping_missing_values_cols(self, df:pd.DataFrame, report_name: str)->pd.DataFrame:
        
        try:
            threshold = self.data_validation_config.missing_threshold
            null_report = df.isna().sum()/df.shape[0]

            logging.info(f"selecting column name which contains null above to {threshold}")
            drop_column_names = null_report[null_report>threshold].index

            logging.info(f"Columns to drop: {list(drop_column_names)}")
            self.validation_error[report_name]=list(drop_column_names)
            df.drop(list(drop_column_names),axis=1,inplace=True)

            logging.info(f"Reading train data frame")
            train_df = pd.read_csv(self.data_ingestion_artifact.data_ingestion_config.train_data_path)
            logging.info(f"Reading test data frame")
            test_df = pd.read_csv(self.data_ingestion_artifact.data_ingestion_config.test_data_path)


            
            if len(df.columns)==0:
                return None
            return df    

        except Exception as e:
            raise CustomException(e, sys)    
        
    def is_required_columns_exists(self, base_df:pd.DataFrame, current_df:pd.DataFrame, report_name: str)-> bool:
        try:
            base_columns = base_df.columns
            current_columns = current_df.columns

            missing_columns = []
            for base_column in base_columns:
                if base_column not in current_columns:
                    logging.info(f"Column: [{base_column} is not available.]")
                    missing_columns.append(base_column)

            if len(missing_columns)>0:
                self.validation_error[report_name]=missing_columns
                return False
            return True

        except Exception as e:
            raise CustomException(e, sys)
        
    def data_drift(self,base_df:pd.DataFrame,current_df:pd.DataFrame,report_key_name:str):
        try:
            drift_report = {}
            base_columns = base_df.columns
            current_columns = current_df.columns

            for base_column in base_columns:
                base_data, current_data = base_df[base_column], current_df[base_column]
                same_distribution =ks_2samp(base_data,current_data)

                if same_distribution.pvalue>0.05:
                    drift_report[base_column] = {
                        "pvalues":float(same_distribution.pvalue),
                        "same_distribution":True
                    }

                else:
                    drift_report[base_column]={
                        "pvalues":float(same_distribution.pvalue),
                        "same_distribution":False
                    }
                self.validation_error[report_name]=drift_report        

        except Exception as e:
            raise CustomException(e, sys)

    def initiate_data_validation(self)->DataValidationArtifact:
        try:
            logging.info("reading base df")
            base_df = pd.read_csv("notebook/data/backorder_dataset.csv")
            base_df.replace({"na":np.NAN},inplace=True)
            logging.info(f"Replace na value in base df")

            logging.info(f"Drop null values columns from base df")
            base_df=self.dropping_missing_values_cols(df=base_df,report_name="missing_values_within_base_dataset")

            logging.info(f"Reading train data frame")
            train_df = pd.read_csv(self.data_ingestion_artifact.data_ingestion_config.train_data_path)
            logging.info(f"Reading test data frame")
            test_df = pd.read_csv(self.data_ingestion_artifact.data_ingestion_config.test_data_path)

            train_df = self.dropping_missing_values_cols(df=train_df, report_name="missing_values_within_train_dataset")
            test_df = self.dropping_missing_values_cols(df=test_df, report_name="missing_values_within_test_dataset")

            exclude_columns = [TARGET_COLUMN]
            base_df = convert_columns_float(df=base_df, exclude_columns=exclude_columns)
            train_df = convert_columns_float(df=train_df, exclude_columns=exclude_columns)
            test_df = convert_columns_float(df=test_df, exclude_columns=exclude_columns)

            logging.info(f"Is all required columns present in train df")
            train_df_columns_status = self.is_required_columns_exists(base_df=base_df, current_df=train_df,report_name="missing_columns_within_train_dataset")
            logging.info(f"Is all required columns present in test df")
            test_df_columns_status = self.is_required_columns_exists(base_df=base_df, current_df=test_df,report_name="missing_columns_within_test_dataset")

            if train_df_columns_status:
                logging.info(f"As all column are available in train df hence detecting data drift")
                self.data_drift(base_df=base_df, current_df=train_df,report_key_name="data_drift_within_train_dataset")
            if test_df_columns_status:
                logging.info(f"As all column are available in test df hence detecting data drift")
                self.data_drift(base_df=base_df, current_df=test_df,report_key_name="data_drift_within_test_dataset")

            #write the report
            logging.info("Write report in yaml file")
            write_yaml_file(file_path=self.data_validation_config.report_file_path,
            data=self.validation_error)

            data_validation_artifact = artifacts_entity.DataValidationArtifact(report_file_path=self.data_validation_config.report_file_path)
            logging.info(f"Data validation artifact: {data_validation_artifact}")
            return data_validation_artifact

        except Exception as e:
            raise CustomException(e, sys)
        


    