import json


def test_token(test_app):
    test_data = {"username": "test_token", "password": "test_token"}
    test_response = {"username": "test_token"}

    response = test_app.post("/user", data=json.dumps(test_data),)
    assert response.status_code == 201
    assert response.json() == test_response

    response = test_app.post("/token", data=test_data,)
    assert response.json()["token_type"] == "bearer"
