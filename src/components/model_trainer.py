import pandas as pd
import os
import sys
from dataclasses import dataclass

from sklearn.linear_model import LinearRegression,Lasso,Ridge
from sklearn.ensemble import RandomForestRegressor,AdaBoostRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import GridSearchCV
from xgboost import XGBRegressor

from src.utils import save_object
from src.logger import logging
from src.exception import CustomException


@dataclass
class ModelTrainerConfig:
    model_object_path = os.path.join("artifacts","model.pkl")
    models_to_train = {
        'LinearRegression':{
            'model':LinearRegression(),
            'params':{},
        },
        'Lasso':{
            'model':Lasso(),
            'params':{
                'alpha':[0.0001, 0.001, 0.01, 0.1, 1, 10, 100]
                }
        },
        'Ridge':{
            'model':Ridge(),
            'params':{
                'alpha':[0.0001, 0.001, 0.01, 0.1, 1, 10, 100]
                }
        },
        'DecisionTreeRegressor':{
            'model':DecisionTreeRegressor(),
            'params':{
                'max_depth':[2, 3, 5, 7, 10, 15, 20, None] ,
                'max_features':[None,'sqrt']
            }
        },
        'RandomForestRegressor':{
            'model':RandomForestRegressor(),
            'params':{
                'n_estimators':[10, 50, 100, 150, 200, 300, 500],
            }
        },
        'AdaBoostRegressor':{
            'model':AdaBoostRegressor(),
            'params':{
                'learning_rate':[0.01, 0.05, 0.1, 0.3, 0.5, 0.8, 1,2]
            }
        },
        'XGBRegressor':{
            'model':XGBRegressor(),
            'params':{}
        }
    }


class ModelTrainer:
    def __init__(self):
        self.model_config = ModelTrainerConfig()

    def train_model(self,train,test):
        try:
            logging.info("Splitting input & output for Model Training...")

            X_train = train[:,:-1]
            X_test = test[:,:-1]

            y_train = train[:,-1]
            y_test = test[:,-1]

            model_evals = []

            print("Finding the best model...")
            logging.info("Finding the best model...")
            
            for name,model in self.model_config.models_to_train.items():
                grid = GridSearchCV(
                    estimator=model['model'],
                    param_grid=model['params'],
                    cv=10
                )

                grid.fit(X_train,y_train)

                current_best = {
                    'model': name,
                    'params' : grid.best_params_,   
                    'score' : grid.best_score_,
                    'estimator':grid.best_estimator_
                }
                
                model_evals.append(current_best)

            best_model = pd.DataFrame(model_evals).sort_values(by='score',ascending=False).iloc[0]

            model_obj = best_model.estimator
            
            logging.info("Saving the best model...")

            save_object(
                self.model_config.model_object_path,
                model_obj
            )
            logging.info("Training the model...")
            model_obj.fit(X_train,y_train)

            model_score = model_obj.score(X_test,y_test)
            if model_score<0.6:
                raise CustomException("Could not find a model fitting the given data.")
            logging.info("Model Returned")
            return (model_score)

        except Exception as e:
            raise CustomException(e,sys)


