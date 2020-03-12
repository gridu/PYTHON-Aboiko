from collections import namedtuple
from application.util import generate_hash
from hmac import compare_digest

from tests.test_data import *


def get_test_token(client):
    response = client.get("/login", json={"login": test_login, "password": test_password})
    return response.headers['x-access-token']


def test_get_centers_unauth(client):
    response = client.get("/centers")
    assert response.status_code == 200


def test_get_center(client):
    response = client.get("/centers/1")
    assert response.status_code == 200


def test_register(client, session):
    response = client.post("/register", json={"login": test_login_register,
                                              "password": test_password_register,
                                              "address": test_address})
    assert response.status_code == 201
    result = session.execute("select * from center where login = :value", {'value': test_login_register})
    Record = namedtuple('Record', result.keys())
    records = [Record(*r) for r in result.fetchall()]
    r = records[0]
    assert r.login == test_login_register
    assert r.address == test_address
    compare_digest(r.password, generate_hash(test_password_register))


def test_token_required(client):
    response = client.get("/animals")
    assert response.status_code == 401


def test_get_animals(client):
    animals_response = client.get("/animals", headers={'x-access-token': 'wrong_value'})
    assert animals_response.json['error'] == 'Token is invalid!'
    assert animals_response.status_code == 401

    animals_response = client.get("/animals")
    assert animals_response.json['error'] == 'Token is missing!'
    assert animals_response.status_code == 401

    token = get_test_token(client)
    animals_response = client.get("/animals", headers={'x-access-token': token})
    assert animals_response.status_code == 200


def test_post_animal(client, session):
    token = get_test_token(client)

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
    result = session.execute("select * from animal where name = :value", {'value': test_animal_name})
    Record = namedtuple('Record', result.keys())
    records = [Record(*r) for r in result.fetchall()]
    r = records[0]
    assert r.age == test_animal_age
    assert r.specie == test_animal_specie


def test_get_animal_for_the_center(client):
    token = get_test_token(client)
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
