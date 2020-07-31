import json


def test_proxy(test_app):
    test_data = {"username": "test_token_proxy", "password": "test_token"}
    test_response = {"username": "test_token_proxy"}

    response = test_app.post("/user", data=json.dumps(test_data),)
    assert response.status_code == 201
    assert response.json() == test_response

    response = test_app.post("/token", data=test_data,)
    assert response.json()["token_type"] == "bearer"

    headers = {
        "Authorization": response.json()["token_type"]
        + " "
        + response.json()["access_token"]
    }
    proxy_data = {"link": "https://postman-echo.com/post/"}
    response = test_app.post("/", data=json.dumps(proxy_data), headers=headers)

    assert response.json()["link"] == proxy_data["link"]
    assert response.json()["is_done"] == True
