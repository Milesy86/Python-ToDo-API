import json
from models.user import User
from sqlalchemy import select

class TestRegister:

    def test_register_success(self, client, session):
        # Test successful registration
        data = {
            "username": "testuser",
            "password": "testpass"
        }
        response = client.post("/register", data=json.dumps(data), content_type="application/json")
        assert response.status_code == 201
        assert response.json == {"msg": "User registered successfully"}

        user = session.execute(select(User).filter_by(username="testuser")).scalar_one()
        assert user is not None
        assert user.username == "testuser"
        assert user.password != "testpass"  # password should be hashed

    def test_register_already_exists(self, client, session):
        # Test registering a duplicate username
        data = {
            "username": "testuser",
            "password": "testpass"
        }
        response = client.post("/register", data=json.dumps(data), content_type="application/json")
        response = client.post("/register", data=json.dumps(data), content_type="application/json")
        assert response.status_code == 400
        assert response.json == {"error": "User already exists"}

    def test_register_missing_password(self, client):
        # Test registering with missing password
        data = {
            "username": "testuser"
        }
        response = client.post("/register", data=json.dumps(data), content_type="application/json")
        assert response.status_code == 400
        assert response.json["error"] == "Username and password are required"

    def test_register_missing_username(self, client):
        # Test registering with missing username
        data = {
            "password": "testpass"
        }
        response = client.post("/register", data=json.dumps(data), content_type="application/json")
        assert response.status_code == 400
        assert response.json["error"] == "Username and password are required"

    def test_register_missing_username_and_password(self, client):
        # Test registering with missing username and password
        data = {}
        response = client.post("/register", data=json.dumps(data), content_type="application/json")
        assert response.status_code == 400
        assert response.json["error"] == "Username and password are required"