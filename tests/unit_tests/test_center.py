from application.logic.center_logic import add_center, login_center
from tests.test_data import *


def test_login_center(test_app, mocker):
    mocker.patch("application.logic.center_logic.does_exist", return_value=True)
    mocker.patch("application.logic.center_logic.validate_credentials", return_value=True)
    mocker.patch("application.logic.center_logic.get_token", return_value=test_token)

    mocker.patch("application.logic.center_logic.insert_request_access_to_db",
                 return_value="Transaction completed successfully")

    with test_app.app_context():
        response = login_center(not_existing_login, "pas1")
    assert response.status_code == 200 \
           and 'x-access-token' in response.headers


def test_add_center(test_app, mocker):
    mocker.patch("application.logic.center_logic.does_exist", return_value=False)
    with test_app.app_context():
        response = add_center(test_login, test_password, test_address)
    assert response.status_code == 201
