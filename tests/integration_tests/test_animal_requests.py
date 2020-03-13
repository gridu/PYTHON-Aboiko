from tests.conftest import get_test_token
from tests.test_data import *


def test_get_animals(client, session):
    animals_response = client.get("/animals", headers={'x-access-token': 'wrong_value'})
    assert animals_response.json['error'] == 'Token is invalid!'
    assert animals_response.status_code == 401

    animals_response = client.get("/animals")
    assert animals_response.json['error'] == 'Token is missing!'
    assert animals_response.status_code == 401

    token = get_test_token(client)
    animals_response = client.get("/animals", headers={'x-access-token': token})

    result = session.execute("select a.id, c.login "
                             " from animal as a "
                             " inner join center as c"
                             " on a.center_id = c.id"
                             " where c.login = :value "
                             , {'value': test_login})
    rows = result.fetchall()
    assert animals_response.status_code == 200 and \
           len(animals_response.get_json()['animals']) == len(rows)


def test_post_animal(client, session):
    token = get_test_token(client)

    # post an animal of not existing specie
    animals_response = client.post("/animals", headers={'x-access-token': token},
                                   json={"name": test_animal_name, "age": test_animal_age,
                                         "specie": "not exists"})
    assert animals_response.status_code == 409

    # malformed JSON in request body
    animals_response = client.post("/animals", headers={'x-access-token': token},
                                   json={"nam": test_animal_name, "age": test_animal_age,
                                         "specie": test_animal_specie})
    assert animals_response.status_code == 400

    # correct request body; first check - animal is absent in db, second check - the animal was added

    result = session.execute("select a.name, c.login "
                             " from animal as a "
                             " inner join center as c"
                             " on a.center_id = c.id"
                             " where c.login = :value0 "
                             " and a.name = :value1"
                             , {'value0': test_login,
                                'value1': test_animal_name})
    rows = result.fetchall()
    assert len(rows) == 0

    animals_response = client.post("/animals", headers={'x-access-token': token},
                                   json={"name": test_animal_name, "age": test_animal_age,
                                         "specie": test_animal_specie})
    assert animals_response.status_code == 201

    # get just added animal from database with raw SQL query
    result = session.execute("select a.name, a.age, a.specie, c.login "
                             " from animal as a "
                             " inner join center as c"
                             " on a.center_id = c.id"
                             " where c.login = :value0 "
                             " and a.name = :value1"
                             , {'value0': test_login,
                                'value1': test_animal_name})
    row = result.first()
    assert row.age == test_animal_age and \
           row.specie == test_animal_specie and \
           row.name == test_animal_name and \
           row.login == test_login

    # post already existing animal (retry the same request in the same test)
    animals_response = client.post("/animals", headers={'x-access-token': token},
                                   json={"name": test_animal_name, "age": test_animal_age,
                                         "specie": test_animal_specie})
    assert animals_response.status_code == 409


def test_get_animal_for_the_center(client, session):
    token = get_test_token(client)
    animals_response = client.get("/animals/" + str(test_animal_id_for_login), headers={'x-access-token': token})
    result = session.execute("select * from animal where id = :value", {'value': test_animal_id_for_login})
    rows = result.fetchall()
    assert animals_response.get_json()['name'] == rows[0].name and \
           animals_response.get_json()['age'] == rows[0].age and \
           animals_response.get_json()['specie'] == rows[0].specie and \
           animals_response.status_code == 200

    # trying to get an animal from another center collection
    animals_response = client.get("/animals/4", headers={'x-access-token': token})
    assert animals_response.status_code == 409 and \
           animals_response.json['error'] == 'you\'re trying to view the animal which isn\'t related to your id'

    # trying to get not existing animal
    animals_response = client.get("/animals/25", headers={'x-access-token': token})
    assert animals_response.status_code == 404 and \
           animals_response.json['error'] == 'you\'re looking for an animal which doesn\'t exist'


def test_delete_animal(client, session):
    token = get_test_token(client)
    animals_response = client.delete("/animals/3", headers={'x-access-token': token})
    assert animals_response.status_code == 200 and \
           animals_response.json['success'] == "an animal deleted successfully"
    result = session.execute("select * from animal where id = :value", {'value': 3})
    rows = result.fetchall()
    assert len(rows) == 0

    animals_response = client.delete("/animals/4", headers={'x-access-token': token})
    assert animals_response.status_code == 409 and \
           animals_response.json['error'] == 'you\'re trying to delete an animal which isn\'t related to your id'

    animals_response = client.delete("/animals/44", headers={'x-access-token': token})
    assert animals_response.status_code == 404 and \
           animals_response.json['error'] == 'you\'re trying to delete an animal which doesn\'t exist'


def test_update_animal(client, session):
    token = get_test_token(client)
    result = session.execute("select * from animal where id = :value", {'value': test_animal_id_for_login})
    rows = result.fetchall()
    name_before = rows[0].name
    age_before = rows[0].age
    specie_before = rows[0].specie
    response = client.put("/animals/" + str(test_animal_id_for_login), json={"name": test_animal_name,
                                                                             "age": test_animal_age,
                                                                             "specie": test_animal_specie},
                          headers={'x-access-token': token})
    result = session.execute("select * from animal where id = :value", {'value': test_animal_id_for_login})
    rows = result.fetchall()
    assert name_before != rows[0].name \
           and age_before != rows[0].age \
           and specie_before != rows[0].specie
