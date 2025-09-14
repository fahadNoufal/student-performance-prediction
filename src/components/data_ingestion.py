import os
import sys
import pandas as pd
from sklearn.model_selection import train_test_split
from dataclasses import dataclass

from src.exception import CustomException
from src.logger import logging

@dataclass
class DataIngestionCongig:
    raw_data_path = os.path.join('artifacts','raw.csv')
    train_data_path = os.path.join('artifacts','train.csv')
    test_data_path = os.path.join('artifacts','test.csv')

class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionCongig()

    def initiate_data_ingestion(self):
        logging.info('Starting Data Ingestion...')
        try:
            df = pd.read_csv('notebook/data/stud.csv')

            logging.info('Extracted data from the source...')
            

            os.makedirs(os.path.dirname(self.ingestion_config.raw_data_path),exist_ok=True)
            df.to_csv(self.ingestion_config.raw_data_path)
            
            training_data,testing_data = train_test_split(df,test_size=0.2,random_state=121)

            training_data.to_csv(self.ingestion_config.train_data_path,index=False,header=False)
            testing_data.to_csv(self.ingestion_config.test_data_path,index=False,header=False)

            logging.info("Data Ingestion Completed...")

            return(
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path,
            )
        except Exception as e:
            raise CustomException(e,sys)
        
