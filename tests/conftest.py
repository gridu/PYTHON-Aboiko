import pytest
import sqlalchemy
from sqlalchemy.orm import scoped_session, sessionmaker

from application import create_app
from settings import TestConfig

test_configs = 'settings.TestConfig'


@pytest.fixture
def client():
    test_app = create_app(test_configs)
    return test_app.test_client()


@pytest.fixture
def session():
    engine = sqlalchemy.create_engine(TestConfig.SQLALCHEMY_DATABASE_URI)
    return scoped_session(sessionmaker(bind=engine))
