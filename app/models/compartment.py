from flask_sqlalchemy import SQLAlchemy
from SQLAlchemy import Column, Integer, ForeignKey

db = SQLAlchemy()

class Compartment(db.Model):
    __tablename__ = 'compartment'

    id = Column(Integer, primary_key=True, autoincrement=True)
    locker_id = Column(Integer, ForeignKey('locker.id'), nullable=False)
    number = Column(Integer, nullable=False)

    def __init__(self, locker_id, number):
        self.locker_id = locker_id
        self.number = number

    def get_number(self):
        return self.number
    
    def get_id(self):
        return str(self.id)