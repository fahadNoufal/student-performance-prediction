from src.logger import logging
from fastapi.responses import JSONResponse,HTMLResponse
from fastapi import FastAPI,Request
from fastapi.templating import Jinja2Templates
from api_model import InputForPrediction
from src.pipeline.predict_pipeline import PredictPipeline
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()


cross_origin_config = {
    "allow_origins": ["*"],
    "allow_credentials": False,
    "allow_methods": ["*"],
    "allow_headers": ["*"],
}
app.add_middleware(
    CORSMiddleware,
    **cross_origin_config
)

templates = Jinja2Templates(directory="templates")

@app.post("/predict")
def predict_score(input:InputForPrediction):
    
    input_for_pred = {
        'gender':input.gender,
        'race_ethnicity':input.race_ethnicity,
        'parental_level_of_education':input.parental_level_of_education,
        'lunch':input.lunch,
        'test_preparation_course':input.test_preparation_course,
        'reading_score':input.reading_score,
        'writing_score':input.writing_score
    }

    pred_pipe = PredictPipeline()
    logging.info(f"Prediction object created")
    prediction = int(pred_pipe.predict(**input_for_pred))
    logging.info(f"Prediction value is: {prediction}")
    return JSONResponse(content={"prediction": prediction})

@app.get("/",response_class=HTMLResponse)
def Home(request: Request):
    return templates.TemplateResponse("index.html",{"request":request})