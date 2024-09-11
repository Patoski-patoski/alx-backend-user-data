#!/usr/bin/env python3
"""DB module"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from user import Base, User


class DB:
    """DB class"""

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Add new user to database
        Args:
            email (str): user email
            hashed_password (str): user hashed_password
        Returns:
            User: User object
        """
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self, **kwargs) -> User:
        """Find user by arbitrary keyword arguments.
        Args:
            **keyword: Arbitrary keyword arguments for filtering.

        Returns:
            User: The first User object found.

        Raises:
            NoResultFound: If no user matches the criteria.
            InvalidRequestError: If invalid query arguments are provided.
        """
        if not kwargs:
            raise InvalidRequestError("No query argument provided")

        query = self._session.query(User)

        for key, value in kwargs.items():
            if not hasattr(User, key):
                raise InvalidRequestError(f"Invalif field: {key}")
            query = query.filter(getattr(User, key) == value)

        user = query.first()
        if user is None:
            raise NoResultFound("No user found matching the criteria")

        return user

    def update_user(self, user_id: int, **kwargs) -> None:
        """To locate the user to update
        Args:
            user_id (int): user id
        """
        try:
            user = self.find_user_by(id=user_id)
        except (NoResultFound, InvalidRequestError, ValueError):
            return

        user = str(user.id)
        for key, value in kwargs.items():
            if not hasattr(User, key):
                raise ValueError(f"Invalid field: {key}")
            setattr(User, user, value)
