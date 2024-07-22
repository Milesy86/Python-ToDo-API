Nathan's Python ToDo List API App
This application consists of a number of API endpoints and was written for a coding test that's part of a job interview.
Hopefully it's a good'un!

It's a Flask front end using SQLAlchemy as an ORM interface to a SQLite database.
It exposes a number of API endpoints allowing users to do things like register, log in, add, modify and delete tasks from the ToDo list.

To run the application:
Clone this repository (git clone https://github.com/Milesy86/Python-ToDo-API.git)

Run locally in Terminal (Windows)
Install Python 3.8 (or higher), if you don't already have it
Open the project in your IDE of choice
Create and activate a python virtual environment, then install dependencies:
python -m venv venv
.\venv\Scripts\activate
pip install -r .\requirements.txt
Run the application:
python app.py

Running the tests
Unit tests have been written using pytest. To run them, you can simply run this in your Terminal:
pytest

To get a test coverage report, run:
coverage run -m pytest
coverage report --show-missing