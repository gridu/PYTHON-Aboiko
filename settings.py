import sys

from flask import Flask
import configparser
import os

this_folder = os.path.dirname(os.path.abspath(__file__))
config_file = os.path.join(this_folder, 'config.ini')

app = Flask(__name__)

parser = configparser.ConfigParser()
parser.read(config_file)


def generate_key():
    return os.urandom(24)


class Config:
    try:
        file_path = os.path.abspath(os.getcwd()) + parser.get('default', 'file_path')
        SQLALCHEMY_DATABASE_URI = 'sqlite:///' + file_path
        SQLALCHEMY_TRACK_MODIFICATIONS = parser.get('default', 'SQLALCHEMY_TRACK_MODIFICATIONS')
        JWT_ALGORITHM = parser.get('default', 'JWT_ALGORITHM')
        JWT_SECRET_KEY = generate_key()

    except configparser.NoOptionError:
        print('could not read configuration file')
        sys.exit(1)


class TestConfig:
    try:
        file_path = os.path.abspath(os.getcwd()) + parser.get('test', 'file_path')
        SQLALCHEMY_DATABASE_URI = 'sqlite:///' + file_path
        SQLALCHEMY_TRACK_MODIFICATIONS = parser.get('test', 'SQLALCHEMY_TRACK_MODIFICATIONS')
        JWT_ALGORITHM = parser.get('default', 'JWT_ALGORITHM')
        JWT_SECRET_KEY = generate_key()

    except configparser.NoOptionError:
        print('could not read configuration file')
        sys.exit(1)
