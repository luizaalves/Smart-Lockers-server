from flask_sqlalchemy import SQLAlchemy
from SQLAlchemy import Column, Integer, String

db = SQLAlchemy()

class Lockers(db.Model):
    __tablename__ = 'locker'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String,nullable=False)

    def __init__(self, name):
        self.name = name

    def get_name(self):
        return str(self.name)
    
    def get_id(self):
        return str(self.id)