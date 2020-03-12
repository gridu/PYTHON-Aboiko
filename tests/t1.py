import os
from collections import namedtuple

from application import create_app
from application.util import generate_hash
from settings import config_file, TestConfig

import sqlalchemy
from sqlalchemy.orm import sessionmaker, scoped_session
from hmac import compare_digest

test_configs = 'settings.TestConfig'

engine = sqlalchemy.create_engine(TestConfig.SQLALCHEMY_DATABASE_URI)
session = scoped_session(sessionmaker(bind=engine))
s = session()

test_login_register = "Center23"
test_password_register = "password23"
test_address = "Berlin"

test_login = "Center1"
test_password = "password1"

test_animal_name = "Gregg"
test_animal_age = 3
test_animal_specie = "red fox"

test_app = create_app(test_configs)


def test_post_animal():
    client = app.test_client()
    response = client.get("/login", json={"login": test_login, "password": test_password})
    token = response.headers['x-access-token']
    animals_response = client.post("/animals", headers={'x-access-token': token},
                                   json={"name": test_animal_name, "age": test_animal_age,
                                         "specie": test_animal_specie})

    result = s.execute("select * from animal where name = :value", {'value': test_animal_name})

    Record = namedtuple('Record', result.keys())
    records = [Record(*r) for r in result.fetchall()]
    print(records)


if __name__ == "__main__":
    test_app.run(debug=True)
    test_post_animal(test_app)
