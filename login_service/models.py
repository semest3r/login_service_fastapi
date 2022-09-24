from sqlalchemy import String, Column, Integer

from .settings import Base

class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    firstname = Column(String, unique=True)
    lastname = Column(String, unique=True)
    password = Column(String, unique=True, nullable=False)