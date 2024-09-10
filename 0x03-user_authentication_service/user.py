#!/usr/bin/env python3
"""user module"""

# In this task you will create a SQLAlchemy model named User for a database
# table named users (by using the mapping declaration of SQLAlchemy).
# The model will have the following attributes:
#   id, the integer primary key
#   email, a non-nullable string
#   hashed_password, a non-nullable string
#   session_id, a nullable string
#   reset_token, a nullable string

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, VARCHAR


Base = declarative_base()


class User(Base):
    """User Model: declarative base class
    Args:
        Base (Base): Base class(declarative)
    """

    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(VARCHAR(250), nullable=False)
    hashed_password = Column(VARCHAR(250), nullable=False)
    session_id = Column(VARCHAR(250))
    reset_token = Column(VARCHAR(250))
