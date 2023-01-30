from typing import Generator

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture(scope="module")
def test_data():
    return [
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


@pytest.fixture()
def client() -> Generator:
    with TestClient(app) as _client:
        yield _client
        app.dependency_overrides = {}
