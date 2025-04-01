import unittest
from app import create_app
from . import main, webapi

app = create_app('testing')

def main_():
    main.main_(app)
    webapi.main_(app)

def get_application():
    return app
