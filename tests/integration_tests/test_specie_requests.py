from tests.conftest import get_test_token
from tests.test_data import *


def test_get_specie(client, session):
    species_response = client.get("/species/" + str(test_specie_id))
    result = session.execute("select * from specie where id = :value", {'value': test_specie_id})
    row = result.first()
    assert species_response.get_json()['name'] == row.name and \
           species_response.get_json()['price'] == row.price and \
           species_response.get_json()['description'] == row.description and \
           species_response.status_code == 200

    # trying to get not existing specie
    species_response = client.get("/species/" + str(test_specie_not_existing_id))
    assert species_response.status_code == 404 and \
           species_response.json['error'] == 'Specie you\'re looking for doesn\'t exist'


def test_get_species(client, session):
    species_response = client.get("/species", headers={'x-access-token': 'wrong_value'})
    assert species_response.json['error'] == 'Token is invalid!'
    assert species_response.status_code == 401

    species_response = client.get("/species")
    assert species_response.json['error'] == 'Token is missing!'
    assert species_response.status_code == 401

    token = get_test_token(client)
    species_response = client.get("/species", headers={'x-access-token': token})

    result = session.execute("select name from specie")
    rows = result.fetchall()
    assert species_response.status_code == 200 and \
           len(species_response.get_json()['species']) == len(rows)


def test_post_specie(client, session):
    token = get_test_token(client)

    # check that specie doesn't exist yet
    result = session.execute("select name, price, description from specie"
                             " where name = :value0 and "
                             " price = :value1 and "
                             " description = :value2"
                             , {'value0': test_specie_name_for_post,
                                'value1': test_specie_price_for_post,
                                'value2': test_specie_description_for_post})
    rows = result.fetchall()
    assert len(rows) == 0

    # post a specie and check that the records were inserted to db
    species_response = client.post("/species", headers={'x-access-token': token},
                                   json={"name": test_specie_name_for_post, "price": test_specie_price_for_post,
                                         "description": test_specie_description_for_post})
    assert species_response.status_code == 201
    result = session.execute("select name, price, description from specie"
                             " where name = :value0 and "
                             " price = :value1 and "
                             " description = :value2"
                             , {'value0': test_specie_name_for_post,
                                'value1': test_specie_price_for_post,
                                'value2': test_specie_description_for_post})
    rows = result.fetchall()
    assert len(rows) == 1 and \
           rows[0].name == test_specie_name_for_post and \
           rows[0].price == test_specie_price_for_post and \
           rows[0].description == test_specie_description_for_post

    # post already existing animal (retry the same request in the same test)
    species_response = client.post("/species", headers={'x-access-token': token},
                                   json={"name": test_specie_name_for_post, "price": test_specie_price_for_post,
                                         "description": test_specie_description_for_post})
    assert species_response.status_code == 409 and \
           species_response.json['error'] == 'That specie already exists'