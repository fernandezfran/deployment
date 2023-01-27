import typing as t

import numpy as np
import pandas as pd
import pydantic

from model.config.core import config
from model.processing.data_manager import _pre_pipeline_preparation


def validate_inputs(
    *, input_data: pd.DataFrame
) -> t.Tuple[pd.DataFrame, t.Optional[dict]]:
    """Check model inputs for unprocessable values."""
    pre_processed = _pre_pipeline_preparation(dataframe=input_data)
    validated_data = pre_processed[config.model_config.features].copy()
    errors = None

    try:
        # replace numpy nans so that pydantic can validate
        MultipleTitanicDataInputs(
            inputs=validated_data.replace({np.nan: None}).to_dict(orient="records")
        )
    except pydantic.ValidationError as error:
        errors = error.json()

    return validated_data, errors


class TitanicDataInputSchema(pydantic.BaseModel):
    pclass: t.Optional[int]
    name: t.Optional[str]
    sex: t.Optional[str]
    age: t.Optional[int]
    sibsp: t.Optional[int]
    parch: t.Optional[int]
    ticket: t.Optional[int]
    fare: t.Optional[float]
    cabin: t.Optional[str]
    embarked: t.Optional[str]
    boat: t.Optional[t.Union[str, int]]
    body: t.Optional[int]


class MultipleTitanicDataInputs(pydantic.BaseModel):
    inputs: t.List[TitanicDataInputSchema]
