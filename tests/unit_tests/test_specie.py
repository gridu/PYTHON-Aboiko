from application.logic.specie_logic import add_specie
from tests.test_data import *


def test_add_specie(test_app, mocker):
    mocker.patch("application.logic.specie_logic.is_specie_exist", return_value=False)

    with test_app.app_context():
        response = add_specie(test_specie_name_exists, test_specie_price_exists, test_specie_description_exists)
    assert response.status_code == 201 and \
           'Location' in response.headers
