# mysql orm 模型的存放

from sqlalchemy.exc import SQLAlchemyError
from flask import current_app
from app import db

class DbSessionCommit():
    @staticmethod
    def add(self):
        db.session.add(self)
        return session_commit()

    @staticmethod
    def update(self):
        return session_commit()

    @staticmethod
    def delete(self):
        db.session.delete(self)
        return session_commit()

class User(db.Model, DbSessionCommit):
    __tablename__ = 't_user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

def session_commit():
    try:
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        reason = str(e)
        current_app.logger.error(reason)
        return reason