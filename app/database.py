# database.py
from flask_sqlalchemy import SQLAlchemy
from enum import Enum
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class UserType(Enum):
    ADMIN = 1
    LIBRARIAN = 2
    GENERAL_USER = 3

class GeneralUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_type = db.Column(db.Enum(UserType), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.String(9), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f'<general_user {self.id} - {self.name}>'
    
    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

