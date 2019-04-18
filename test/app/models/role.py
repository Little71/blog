from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String

from app.models.base import Base


class Role(Base):
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True)
    name = Column(String(64), unique=True)
    users = relationship('User', backref='role')

    def __repr__(self):
        return '<Role %r>' % self.name
