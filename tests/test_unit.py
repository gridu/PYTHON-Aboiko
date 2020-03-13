from tests.test_data import *


def test_login_center(client, mocker):
    mocker.patch("application.validations.center_validations.does_exist", return_value=True)
    mocker.patch("application.validations.center_validations.validate_credentials", return_value=True)
    mocker.patch("application.logic.center_logic.get_token", return_value=test_token)

    response = client.get('/login', json={"login": "Center3",
                                          "password": "password3"})
    assert response.status_code == 200 \
           and 'x-access-token' in response.headers


def test_register_center(client, mocker):
    mocker.patch("application.validations.center_validations.does_exist", return_value=False)
    response = client.post("/register", json={"login": test_login_register,
                                              "password": test_password_register,
                                              "address": test_address})
    assert response.status_code == 201
