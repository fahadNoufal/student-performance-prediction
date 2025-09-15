import os
import sys
import pandas as pd
import numpy as np

from src.logger import logging
from src.exception import CustomException
from src.utils import save_object

from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder,StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from dataclasses import dataclass

@dataclass
class DataTransformationConfig:
        data_preprocessor_path = os.path.join("artifacts",'preprocessor.pkl')

class DataTransformation:
        def __init__(self):
            self.transformation_config = DataTransformationConfig()

        def get_data_transformation_obj(self):
                
            try:
                cat_features = ['gender','race_ethnicity','parental_level_of_education','lunch','test_preparation_course']
                num_features = ['reading_score','writing_score']

                cat_pipeline = Pipeline(
                    steps=[
                            ('SimpleImputer',SimpleImputer(strategy='most_frequent')),
                            ('OneHotEncoding',OneHotEncoder()),
                    ]
                )

                num_pipeline = Pipeline(
                    steps=[
                        ('SimpleImputer',SimpleImputer(strategy='mean')),
                        ('StandardScaling',StandardScaler()),
                    ]
                )


                preprocessor = ColumnTransformer(
                    [
                            ('cat_pipeline',cat_pipeline,cat_features),
                            ('num_pipeline',num_pipeline,num_features)
                    ]
                )

                logging.info('Preprocessor object created')

                return preprocessor
            
            except Exception as e:
                  raise CustomException(e,sys)
            
        def initiate_data_transformation(self,train,test):
            logging.info("Initiating data transformation...")
            try:
                train_set = pd.read_csv(train)
                test_set = pd.read_csv(test)
            
                preprossing_obj = self.get_data_transformation_obj()

                input_train_set = train_set.drop(columns='math_score')
                output_train_set = train_set.math_score

                input_test_set = test_set.drop(columns='math_score')
                output_test_set = test_set.math_score

                logging.info("Extracting data for transformation...")

                input_train_data = preprossing_obj.fit_transform(input_train_set)
                input_test_data = preprossing_obj.transform(input_test_set)

                training_data = np.c_[input_train_data,np.array(output_train_set)]
                testing_data = np.c_[input_test_data,np.array(output_test_set)]
                
                logging.info("Exporting preprocessing object...")

                save_object(self.transformation_config.data_preprocessor_path,preprossing_obj)

                logging.info("Preprocessing completed") 

                return(
                     training_data,
                     testing_data,
                    #  self.transformation_config.data_preprocessor_path
                )
            
            except Exception as e:
                 raise CustomException(e,sys)
            
                 