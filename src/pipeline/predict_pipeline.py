import os
import sys
from dataclasses import dataclass,asdict
import pandas as pd
from src.exception import CustomException
from src.logger import logging
from src.utils import load_object



@dataclass
class CustomInput:
    gender:str
    race_ethnicity:str
    parental_level_of_education:str
    lunch:str
    test_preparation_course:str
    reading_score:int
    writing_score:int

    def as_df(self):
        return pd.DataFrame([asdict(self)])


class PredictPipeline:

    def predict(self,gender:str,race_ethnicity:str,parental_level_of_education:str,lunch:str,test_preparation_course:str,reading_score:int,writing_score:int):
        try:
            logging.info("Initializing prediction...")

            self.custom_input = CustomInput(
                gender=gender,
                race_ethnicity=race_ethnicity,
                parental_level_of_education=parental_level_of_education,
                lunch=lunch,
                test_preparation_course=test_preparation_course,
                reading_score=reading_score,
                writing_score=writing_score
            )

            input_df = self.custom_input.as_df()

            logging.info("Importing model and preprocessor for prediction...")

            model_path = os.path.join("artifacts","model.pkl")
            preprocessor_path = os.path.join("artifacts","preprocessor.pkl")

            model = load_object(model_path)
            preprocessor = load_object(preprocessor_path)

            input_data = preprocessor.transform(input_df)
            logging.info("Prediction based on input")
            predicted = model.predict(input_data)

            predicted = min(predicted,100)
            predicted = max(predicted,0)

            return(
                predicted
            )
        except Exception as e:
            raise CustomException(e,sys)    
