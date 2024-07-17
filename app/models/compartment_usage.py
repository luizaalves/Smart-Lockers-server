from flask_sqlalchemy import SQLAlchemy
from SQLAlchemy import Column, Integer, ForeignKey, DateTime

db = SQLAlchemy()

class CompartmentUsage(db.Model):
    __tablename__ = 'compartmentusage'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    compartment_id = Column(Integer, ForeignKey('compartment.id'), nullable=False)
    open_time = Column(DateTime, nullable=False)
    close_time = Column(DateTime, nullable=False)
    retrieve_time = Column(DateTime, nullable=False)
    end_retrieve_time = Column(DateTime, nullable=False)

    def __init__(self, id_user, id_compartment, open_time, close_time):
        self.user_id = id_user
        self.compartment_id = id_compartment
        self.open_time = open_time
        self.close_time = close_time

    def set_removal_time(self, retrieve_time, end_retrieve_time):
        self.retrieve_time = retrieve_time
        self.end_retrieve_time = end_retrieve_time
    
    def get_id(self):
        return str(self.id)