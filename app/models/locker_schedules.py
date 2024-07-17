from flask_sqlalchemy import SQLAlchemy
from SQLAlchemy import Column, Integer, ForeignKey, DateTime

db = SQLAlchemy()

class LockerSchedules(db.Model):
    __tablename__ = 'lockerschedule'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    compartment_id = Column(Integer, ForeignKey('compartment.id'), nullable=False)
    open_time = Column(DateTime, nullable=False)
    close_time = Column(DateTime, nullable=False)
    retrieve_time = Column(DateTime, nullable=False)
    end_retrieve_time = Column(DateTime, nullable=False)

    def __init__(self, id_user, id_compartment, date_opening):
        self.user_id = id_user
        self.compartment_id = id_compartment
        self.opening_date = date_opening

    def set_removal_date(self, date_removal):
        self.removal_date = date_removal
        return self.removal_date
    
    def get_id(self):
        return str(self.id)