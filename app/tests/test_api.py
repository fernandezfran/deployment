from fastapi.testclient import TestClient


def test_make_prediction(client: TestClient, test_data) -> None:
    # Given
    payload = {"inputs": test_data}

    # When
    response = client.post(
        "http://localhost:8001/api/v1/predict",
        json=payload,
    )
    prediction_data = response.json()
    print(prediction_data)

    # Then
    assert response.status_code == 200
    prediction_data = response.json()
    assert prediction_data["predictions"]
    assert prediction_data["errors"] is None
    assert prediction_data["predictions"][0] == 1
