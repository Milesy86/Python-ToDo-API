from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash
from database import database

class User(database.Model):
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

    tasks = relationship("Task", back_populates="user")

    # Store a hash of the the user's chosen password 
    def set_password(self, password):
        self.password = generate_password_hash(password)