import json
import typing as t

import fastapi
import loguru
import numpy as np
import pandas as pd
from model import __version__ as model_version
from model.predict import make_prediction

from app import __version__, schemas
from app.config import settings

api_router = fastapi.APIRouter()


@api_router.get("/health", response_model=schemas.Health, status_code=200)
def health() -> dict:
    """Root Get."""
    health = schemas.Health(
        name=settings.PROJECT_NAME, api_version=__version__, model_version=model_version
    )

    return health.dict()


@api_router.post("/predict", response_model=schemas.PredictionResults, status_code=200)
async def predict(input_data: schemas.MultipleTitanicDataInputs) -> t.Any:
    """Make survival titanic predictions with the TID classification model."""

    input_df = pd.DataFrame(fastapi.encoders.jsonable_encoder(input_data.inputs))

    # Advanced: You can improve performance of your API by rewriting the
    # `make prediction` function to be async and using await here.
    loguru.logger.info(f"Making prediction on inputs: {input_data.inputs}")
    results = make_prediction(input_data=input_df.replace({np.nan: None}))

    if results["errors"] is not None:
        loguru.logger.warning(f"Prediction validation error: {results.get('errors')}")
        raise fastapi.HTTPException(
            status_code=400, detail=json.loads(results["errors"])
        )

    loguru.logger.info(f"Prediction results: {results.get('predictions')}")

    return results
