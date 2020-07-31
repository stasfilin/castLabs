import json


def test_user(test_app):
    test_data = {"username": "test", "password": "test"}
    test_response = {"username": "test"}

    response = test_app.post("/user", data=json.dumps(test_data),)
    assert response.status_code == 201
    assert response.json() == test_response
