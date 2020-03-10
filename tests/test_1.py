import os

import pytest
# from flaskr.db import get_db
from application import create_app
from application.models.center import Center
from settings import config_file


@pytest.fixture
def setup():
    app = create_app()
    return app


def test_config_path_correct(setup):
    assert os.path.exists(config_file)


def test_get_centers_unauth(setup):
    client = setup.test_client()
    response = client.get("/centers")
    assert response.status_code == 200


def test_get_center(setup):
    client = setup.test_client()
    response = client.get("/centers/1")
    assert response.status_code == 200


def test_register(setup):
    client = setup.test_client()
    response = client.post("/register", json={"login": "Center23", "password": "password23", "address": "Berlin"})
    assert response.status_code == 201
    with setup.app_context():
        assert (
                Center.query.filter_by(login="Center23").one_or_none() is not None
        )


def test_get_token_with_login(setup):
    client = setup.test_client()
    response = client.get("/login", json={"login": "Center2", "password": "password2"})
    assert response.status_code == 200
    token = response.headers['x-access-token']
    assert token is not None


def test_token_required(setup):
    client = setup.test_client()
    response = client.get("/animals")
    assert response.status_code == 401


def test_token(setup):
    client = setup.test_client()
    response = client.get("/login", json={"login": "Center2", "password": "password2"})
    token = response.headers['x-access-token']
    animals_response = client.get("/animals", headers={'x-access-token': token})
    assert animals_response.status_code == 200
