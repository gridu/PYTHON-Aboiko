from application.logic.animal_logic import delete_animal, get_animal, add_animal, update_animal
from tests.test_data import *


def test_get_animal(test_app, mocker):
    # mocking the function which validates center id
    mocker.patch("application.logic.animal_logic.is_center_id_valid", return_value=True)
    with test_app.app_context():
        response = get_animal(test_login, test_animal_id_not_related_for_login)
    assert response.status_code == 200

    with test_app.app_context():
        response = get_animal(test_login, not_existing_animal_id)
    assert response.status_code == 404 and \
        response.json["error"] == "you\'re looking for an animal which doesn\'t exist"


def test_add_animal(test_app, mocker):
    mocker.patch("application.logic.animal_logic.is_center_id_valid", return_value=True)
    mocker.patch("application.logic.animal_logic.is_specie_exist", return_value=True)
    with test_app.app_context():
        response = add_animal(test_login, test_animal_name_exists, test_animal_age_exists, test_animal_specie_exists)
    assert response.status_code == 201 and \
        'Location' in response.headers


def test_delete_animal(test_app, mocker):
    # mocking the function which validates center id
    mocker.patch("application.logic.animal_logic.is_center_id_valid", return_value=True)
    with test_app.app_context():
        response = delete_animal(test_login, test_animal_id_not_related_for_login)
    assert response.status_code == 200 and \
        response.json["success"] == "an animal deleted successfully"

    with test_app.app_context():
        response = delete_animal(test_login, not_existing_animal_id)
    assert response.status_code == 404 and \
        response.json["error"] == "you\'re trying to delete an animal which doesn\'t exist"


def test_update_animal(test_app, mocker):
    mocker.patch("application.logic.animal_logic.is_center_id_valid", return_value=True)
    mocker.patch("application.logic.animal_logic.is_specie_exist", return_value=True)
    with test_app.app_context():
        response = update_animal(test_animal_data_exists)
    assert response.status_code == 200 and \
        response.json["success"] == "an animal updated successfully"

    with test_app.app_context():
        response = update_animal(test_animal_not_existing)
    assert response.status_code == 404 and \
        response.json["error"] == "you\'re trying to update an animal which doesn\'t exist"
