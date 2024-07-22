from flask import Flask
from database import database
from config import Config
from routes import login, register, tasks
from flask_jwt_extended import JWTManager

def create_app(config_object):
    app = Flask(__name__)
    app.config.from_object(config_object)

    database.init_app(app)
    jwt = JWTManager(app)

    # Bring in the blueprints of the API endpoints
    app.register_blueprint(login.bp)
    app.register_blueprint(register.bp)
    app.register_blueprint(tasks.bp)

    return app


if __name__ == "__main__":
    app = create_app(Config)
    # Create the DB & tables if they don't exist. The schema is defined in /models.
    with app.app_context():
        database.create_all()
    # Start the flask app
    app.run(debug=True)