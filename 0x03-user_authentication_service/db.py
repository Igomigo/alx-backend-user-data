#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db")
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
        """Adds and returns a user object
        """
        session = self._session
        user = User(email=email, hashed_password=hashed_password)
        session.add(user)
        session.commit()
        return user

    def find_user_by(self, **kwargs) -> User:
        """Finds and returns a user by email from the database
        """
        if kwargs is None:
            raise InvalidRequestError

        table_columns = User.__table__.columns.keys()

        for key in kwargs.keys():
            if key not in table_columns:
                raise InvalidRequestError

        session = self._session
        user = session.query(User).filter_by(**kwargs).first()

        if user is None:
            raise NoResultFound

        return user

    def update_user(self, id: int, **kwargs) -> None:
        """Updates a user data based on the passed parameter
        """
        if kwargs is None:
            raise InvalidRequestError

        table_columns = User.__table__.columns.keys()
        for key in kwargs.keys():
            if key not in table_columns:
                raise ValueError

        user = self.find_user_by(id=id)
        if user is None:
            raise NoResultFound

        session = self._session
        for key in table_columns:
            if key in kwargs.keys():
                setattr(user, key, kwargs.get(key))

        session.commit()
