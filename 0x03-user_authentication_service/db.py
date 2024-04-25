#!/usr/bin/env python3
"""DB module for database operations.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound

from user import Base, User


class DB:
    """Database class for handling user operations.
    """

    def __init__(self) -> None:
        """Initialize a new DB instance and create necessary tables.
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object for database interactions.
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        '''
        Add a new user to the database.

        Args:
            email (str): The email of the user.
            hashed_password (str): The hashed password of the user.

        Returns:
            User: The user object that has been added to the database.
        '''
        new_user = User(email=email, hashed_password=hashed_password)

        # Add the new user to the session
        self._session.add(new_user)
        self._session.commit()

        return new_user

    def find_user_by(self, **kwargs) -> User:
        '''
        Find a user in the database based on given criteria.

        Args:
            **kwargs: Arbitrary keyword arguments representing
            the search criteria.

        Returns:
            User: The user object found in the database.

        Raises:
            InvalidRequestError: If no search criteria are provided.
            NoResultFound: If no matching user is found.
        '''
        if not kwargs:
            raise InvalidRequestError("No search criteria provided")

        user = self._session.query(User).filter_by(**kwargs).first()
        if not user:
            raise NoResultFound("No user found with the specified criteria")
        return user

    def update_user(self, user_id: int, **kwargs) -> None:
        '''
        Update user's details in the database.

        Args:
            user_id (int): The ID of the user to be updated.
            **kwargs: Arbitrary keyword arguments representing the
            updated details.

        Raises:
            ValueError: If an invalid attribute is provided for update.
        '''
        found_user = self.find_user_by(id=user_id)

        for key, value in kwargs.items():
            if not hasattr(found_user, key):
                raise ValueError(f"Invalid attribute '{key}' \
                                 provided for update")
            setattr(found_user, key, value)

        self._session.commit()
