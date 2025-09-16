from pydantic import BaseModel


class InputForPrediction(BaseModel):
    gender:str
    race_ethnicity:str
    parental_level_of_education:str
    lunch:str
    test_preparation_course:str
    reading_score:int
    writing_score:int

    # { "gender": "female", "race_ethnicity": "group B", "parental_level_of_education": "bachelor's degree", "lunch": "standard", "test_preparation_course": "none", "reading_score": 72, "writing_score": 74 }