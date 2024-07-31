from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from .. import db

class LockerSchedules(db.Model):
    __tablename__ = 'locker_schedule'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    user = relationship('User', back_populates='locker_schedules', lazy=True)
    compartment_id = Column(Integer, ForeignKey('compartment.id'), nullable=False)
    compartment = relationship('Compartment', back_populates='locker_schedules', lazy=True)
    open_time = Column(DateTime, nullable=False)
    close_time = Column(DateTime, nullable=False)
    retrieve_time = Column(DateTime, nullable=False)
    end_retrieve_time = Column(DateTime, nullable=False)

    def __init__(self, id_user, id_compartment, open_time, close_time, retrieve_time, end_retrieve_time):
        self.user_id = id_user
        self.compartment_id = id_compartment
        self.open_time = open_time,
        self.close_time =close_time
        self.retrieve_time = retrieve_time
        self.end_retrieve_time = end_retrieve_time

    def set_removal_date(self, date_removal):
        self.removal_date = date_removal
        return self.removal_date
    
    def get_id(self):
        return str(self.id)