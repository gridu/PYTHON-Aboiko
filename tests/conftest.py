import pytest
import sqlalchemy
from sqlalchemy.orm import scoped_session, sessionmaker
from tests.test_data import *

from application import create_app
from settings import TestConfig

test_configs = 'settings.TestConfig'


@pytest.fixture(scope='session')
def test_app():
    return create_app(test_configs)


@pytest.fixture(scope='function')
def client(test_app):
    return test_app.test_client()


@pytest.fixture(scope='session')
def session():
    engine = sqlalchemy.create_engine(TestConfig.SQLALCHEMY_DATABASE_URI)
    return scoped_session(sessionmaker(bind=engine))


def get_test_token(client):
    response = client.get("/login", json={"login": test_login, "password": test_password})
    return response.headers['x-access-token']
