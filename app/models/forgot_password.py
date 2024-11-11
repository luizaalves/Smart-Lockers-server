from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, ForeignKey, DateTime, String
from sqlalchemy.orm import relationship
from .. import db
from flask import session

class ForgotPassword(db.Model):
    __tablename__ = 'forgot_password'

    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String(6),nullable=False)
    date_time = Column(DateTime, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    user = relationship('User', back_populates='forgot_password', lazy=True)

    def __init__(self, id_user, code_generated, date_time):
        self.user_id = id_user
        self.code = code_generated
        self.date_time = date_time
    
    def get_id(self):
        return str(self.id)