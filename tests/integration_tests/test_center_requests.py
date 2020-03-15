from application.util import verify_hash
from tests.test_data import *


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
    result = session.execute("SELECT * FROM center WHERE login = :value", {'value': test_login_register})
    center = result.first()
    assert center.login == test_login_register
    assert center.address == test_address
    assert verify_hash(test_password_register, center.password) is True
