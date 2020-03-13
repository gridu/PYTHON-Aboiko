from tests.test_data import *


def test_login_center(client, mocker):
    exist_mock = mocker.patch("application.validations.center_validations.does_exist")
    creds_mock = mocker.patch("application.validations.center_validations.validate_credentials")
    token_mock = mocker.patch("application.logic.center_logic.get_token")
    exist_mock.return_value = True
    creds_mock.return_value = True
    token_mock.return_value = test_token
    response = client.get('/login', json={"login": "Dummy login",
                                          "password": "Dummy password"})
    assert response.status_code == 200 \
           and 'x-access-token' in response.headers
