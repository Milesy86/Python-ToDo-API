import json
from models.user import User
from database import database

class TestLogin:

    def test_login_success(self, client, session):
        # Create a test user directly in the db
        user = User(username="testuser", password="testpass")
        user.set_password("testpass")
        session.add(user)
        session.commit()

        # Test logging in as the test user
        data = {
            "username": "testuser",
            "password": "testpass"
        }
        response = client.post("/login", data=json.dumps(data), content_type="application/json")
        assert response.status_code == 200
        assert "token" in response.json

    def test_login_invalid_credentials(self, client, session):
        # Create a test user directly in the db
        user = User(username="testuser", password="testpass")
        user.set_password("testpass")
        session.add(user)
        session.commit()

        # Test logging in with invalid credentials
        data = {
            "username": "testuser",
            "password": "wrongpass"
        }
        response = client.post("/login", data=json.dumps(data), content_type="application/json")
        assert response.status_code == 403
        assert response.json["msg"] == "Authentication Failure"

    def test_login_missing_password(self, client):
        # Test logging in with missing password
        data = {
            "username": "testuser"
        }
        response = client.post("/login", data=json.dumps(data), content_type="application/json")
        assert response.status_code == 400
        assert response.json["error"] == "Username and password are required"

    def test_login_missing_username(self, client):
        # Test logging in with missing username
        data = {
            "password": "testpass"
        }
        response = client.post("/login", data=json.dumps(data), content_type="application/json")
        assert response.status_code == 400
        assert response.json["error"] == "Username and password are required"

    def test_login_missing_username_and_password(self, client):
        # Test logging in with missing username and password
        data = {}
        response = client.post("/login", data=json.dumps(data), content_type="application/json")
        assert response.status_code == 400
        assert response.json["error"] == "Username and password are required"