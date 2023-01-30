from typing import Any, List, Optional

from model.processing.validation import TitanicDataInputSchema
from pydantic import BaseModel


class PredictionResults(BaseModel):
    errors: Optional[Any]
    version: str
    predictions: Optional[List[int]]


class MultipleTitanicDataInputs(BaseModel):
    inputs: List[TitanicDataInputSchema]

    class Config:
        schema_extra = {
            "example": {
                "inputs": [
                    {
                        "pclass": 1,
                        "name": "Andrews, Miss. Kornelia Theodosia",
                        "sex": "female",
                        "age": 63,
                        "sibsp": 1,
                        "parch": 0,
                        "ticket": "13502",
                        "fare": 77.9583,
                        "cabin": "D7",
                        "embarked": "S",
                        "boat": "10",
                        "body": 135,
                    }
                ]
            }
        }
