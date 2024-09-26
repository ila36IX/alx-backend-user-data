#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.session import Session
from typing import Union
from user import User, Base


class DB:
    """DB class
    """

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
        """save the user to the database and return it"""
        user = User(email=email, hashed_password=hashed_password)
        s = self._session
        s.add(user)
        s.commit()
        return user

    def find_user_by(self, **kwargs: Union[str, int]) -> User:
        """Returns the first row found in the users table as filtered by the
        method’s input arguments
        """
        s = self._session
        user = s.query(User).filter_by(**kwargs).one()
        return user

    def update_user(self, user_id: int, **kwargs: Union[str, int]):
        """Update the user’s attributes as passed in the method’s arguments
        then commit changes to the database
        """
        user = self.find_user_by(id=user_id)
        for k, v in kwargs.items():
            if hasattr(user, k):
                setattr(user, k, v)
            else:
                raise ValueError
        self._session.commit()
