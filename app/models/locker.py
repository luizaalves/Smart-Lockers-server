from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from .. import db

class Lockers(db.Model):
    __tablename__ = 'locker'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(20),nullable=False)

    compartments = relationship("Compartment", back_populates='locker', lazy=True)

    def __init__(self, name):
        self.name = name

    def get_name(self):
        return str(self.name)
    
    def get_id(self):
        return str(self.id)