import sys
import os
import pytest
import json
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

# Add the project directory to the sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app
from database import database
from config import Config
from models.user import User
from models.task import Task

@pytest.fixture(scope="module")
def test_app():
    test_config = Config
    test_config.SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    app = create_app(test_config)
    

    with app.app_context():
        database.create_all()
        yield app
        database.session.remove()
        database.drop_all()

@pytest.fixture(scope="module")
def client(test_app):
    return test_app.test_client()

@pytest.fixture(scope="function")
def session(test_app):
    connection = database.engine.connect()
    transaction = connection.begin()
    
    options = dict(bind=connection, binds={})
    Session = scoped_session(sessionmaker(**options))
    database.session = Session

    yield Session

    transaction.rollback()
    connection.close()
    Session.remove()

@pytest.fixture
def get_token(client, session):
    # A fixture to create and login a user, then return the token from the response
    def _get_token(username, password):
        # Create the user in the database
        user = User(username=username)
        user.set_password(password)
        session.add(user)
        session.commit()

        # Request a token
        data = {
            "username": username,
            "password": password
        }
        response = client.post("/login", data=json.dumps(data), content_type="application/json")
        assert response.status_code == 200
        return response.json["token"]

    return _get_token