import os
from collections import namedtuple

import pytest

from application import create_app

from application.util import generate_hash
from settings import config_file, TestConfig

import sqlalchemy
from sqlalchemy.orm import sessionmaker, scoped_session
from hmac import compare_digest

test_configs = 'settings.TestConfig'

test_login_register = "Center23"
test_password_register = "password23"
test_address = "Berlin"

test_login = "Center1"
test_password = "password1"

test_animal_name = "Gregg"
test_animal_age = 3
test_animal_specie = "red fox"


def get_scoped_session():
    engine = sqlalchemy.create_engine(TestConfig.SQLALCHEMY_DATABASE_URI)
    session = scoped_session(sessionmaker(bind=engine))
    return session()


@pytest.fixture
def setup():
    test_app = create_app(test_configs)
    return test_app


def get_test_token(setup):
    client = setup.test_client()
    response = client.get("/login", json={"login": test_login, "password": test_password})
    return response.headers['x-access-token']


def test_config_path_correct():
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
    response = client.post("/register", json={"login": test_login_register,
                                              "password": test_password_register,
                                              "address": test_address})
    assert response.status_code == 201
    s = get_scoped_session()
    result = s.execute("select * from center where login = :value", {'value': test_login_register})
    Record = namedtuple('Record', result.keys())
    records = [Record(*r) for r in result.fetchall()]
    r = records[0]
    assert r.login == test_login_register
    assert r.address == test_address
    compare_digest(r.password, generate_hash(test_password_register))


def test_get_token_with_login(setup):
    token = get_test_token(setup)
    assert token is not None


def test_token_required(setup):
    client = setup.test_client()
    response = client.get("/animals")
    assert response.status_code == 401


def test_token(setup):
    client = setup.test_client()
    token = get_test_token(setup)
    animals_response = client.get("/animals", headers={'x-access-token': token})
    assert animals_response.status_code == 200


def test_post_animal(setup):
    client = setup.test_client()
    token = get_test_token(setup)

    # post an animal of not existin specie
    animals_response = client.post("/animals", headers={'x-access-token': token},
                                   json={"name": test_animal_name, "age": test_animal_age,
                                         "specie": "not exists"})
    assert animals_response.status_code == 409

    # correct request body
    animals_response = client.post("/animals", headers={'x-access-token': token},
                                   json={"name": test_animal_name, "age": test_animal_age,
                                         "specie": test_animal_specie})
    assert animals_response.status_code == 201

    # malformed JSON in request body
    animals_response = client.post("/animals", headers={'x-access-token': token},
                                   json={"nam": test_animal_name, "age": test_animal_age,
                                         "specie": test_animal_specie})
    assert animals_response.status_code == 400

    # post already existing animal (retry the same request in the same test)
    animals_response = client.post("/animals", headers={'x-access-token': token},
                                   json={"name": test_animal_name, "age": test_animal_age,
                                         "specie": test_animal_specie})
    assert animals_response.status_code == 409

    # get just added animal from database with raw SQL query
    s = get_scoped_session()
    result = s.execute("select * from animal where name = :value", {'value': test_animal_name})
    Record = namedtuple('Record', result.keys())
    records = [Record(*r) for r in result.fetchall()]
    r = records[0]
    assert r.age == test_animal_age
    assert r.specie == test_animal_specie


def test_get_animal_for_the_center(setup):
    client = setup.test_client()
    token = get_test_token(setup)
    animals_response = client.get("/animals/3", headers={'x-access-token': token})
    assert animals_response.status_code == 200

    # trying to get an animal from another center collection
    animals_response = client.get("/animals/4", headers={'x-access-token': token})
    assert animals_response.status_code == 409
    assert animals_response.json['error'] == 'you\'re trying to view the animal which isn\'t related to your id'

    # trying to get not existing animal
    animals_response = client.get("/animals/25", headers={'x-access-token': token})
    assert animals_response.status_code == 404
    assert animals_response.json['error'] == 'you\'re looking for an animal which doesn\'t exist'
