import os, sys
from dataclasses import dataclass
import pandas as pd
import numpy as np 
from sklearn.model_selection import train_test_split

from backorder.logger import logging
from backorder.exception import CustomException
from backorder.entity import artifacts_entity
from backorder.entity import config_entity

class DataIngestion:
    def __init__(self):
        self.data_ingestion_config = config_entity.DataIngestionConfig()

    def initiate_data_ingestion(self):
        logging.info("initiating data ingestion")
        try:
            logging.info("read data as data frame")
            df = pd.read_csv("notebook/data/backorder_dataset.csv", low_memory=False)
            os.makedirs(os.path.dirname(self.data_ingestion_config.raw_data_path), exist_ok=True)
            df.sample(2000).to_csv(self.data_ingestion_config.raw_data_path, header=True, index=False)

            logging.info("removing sku column")
            df = df.drop(columns=['sku'], axis=1)

            logging.info("removing duplicates")
            df = df.drop_duplicates(ignore_index=True)

            logging.info("splitting data into train and test and saving it")
            train_set, test_set = train_test_split(df, test_size=0.25, random_state=42)
            train_set.to_csv(self.data_ingestion_config.train_data_path, index=False, header=True)
            test_set.to_csv(self.data_ingestion_config.test_data_path, index=False, header=True)

            logging.info("data ingestion completed")
            return artifacts_entity.DataIngestionArtifacts(
                self.data_ingestion_config.train_data_path,
                self.data_ingestion_config.test_data_path
            )
            
        except Exception as e:
            raise CustomException(e, sys)