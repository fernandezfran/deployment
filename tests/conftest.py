import logging

import pytest
import sklearn.model_selection

from model.config.core import config
from model.processing.data_manager import _load_raw_dataset

logger = logging.getLogger(__name__)


@pytest.fixture()
def sample_input_data():
    data = _load_raw_dataset(file_name=config.app_config.raw_data_file)

    X_train, X_test, y_train, y_test = sklearn.model_selection.train_test_split(
        data,
        data[config.model_config.target],
        test_size=config.model_config.test_size,
        random_state=config.model_config.random_state,
    )

    return X_test
