from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, ForeignKey
from werkzeug.security import generate_password_hash, check_password_hash

from app import login_manager
from app.models.base import Base


class User(UserMixin,Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String(64), unique=True, index=True)
    username = Column(String(64), unique=True, index=True)
    _password = Column('password', String(128))
    role_id = Column(Integer, ForeignKey('roles.id'))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute ')

    @password.setter
    def password(self, password):
        self._password = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self._password, password)

    def __repr__(self):
        return '<User %r>' % self.username

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
