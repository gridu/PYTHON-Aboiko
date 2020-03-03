from flask import Flask
import configparser
import os

app = Flask(__name__)

parser = configparser.ConfigParser()
parser.read('config.ini')


class Config:
    file_path = os.path.abspath(os.getcwd()) + parser.get('default', 'file_path')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + file_path
    SQLALCHEMY_TRACK_MODIFICATIONS = parser.get('default', 'SQLALCHEMY_TRACK_MODIFICATIONS')
    JWT_SECRET_KEY = parser.get('default', 'jwt_secret')
