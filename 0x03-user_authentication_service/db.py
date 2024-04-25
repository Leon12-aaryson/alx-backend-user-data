from user import User
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound


class DB:
    """DB class
    """

    def add_user(self, email: str, hashed_password: str) -> User:
        """Add a new user to the database

        Args:
            email (str): The email of the user
            hashed_password (str): The hashed password of the user

        Returns:
            User: The user object that has been added to the database
        """
        new_user = User(email=email, hashed_password=hashed_password)

        self._session.add(new_user)
        self._session.commit()

        return new_user

    def find_user_by(self, **kwargs) -> User:
        """Find a user in the database based on given criteria

        Args:
            **kwargs: Arbitrary keyword arguments representing
            the search criteria
        Returns:
            User: The user object found in the database

        Raises:
            NoResultFound: If no matching user is found
            InvalidRequestError: If wrong query arguments are passed
        """
        try:
            # Query the database for the first user matching the given criteria
            user = self._session.query(User).filter_by(**kwargs).first()

            # If no user is found, raise NoResultFound
            if user is None:
                raise NoResultFound("No user found with the specified \
                                    criteria")

            return user
        except InvalidRequestError as e:
            # If wrong query arguments are passed, raise InvalidRequestError
            raise InvalidRequestError("Invalid query arguments") from e

    def update_user(self, user_id: int, **kwargs) -> None:
        """Update a user in the database based on user_id and given attributes

        Args:
            user_id (int): The ID of the user to update
            **kwargs: Arbitrary keyword arguments representing the
            attributes to update
        Raises:
            ValueError: If an invalid attribute is passed
        """
        user = self.find_user_by(id=user_id)

        for attr, value in kwargs.items():
            if hasattr(User, attr):
                setattr(user, attr, value)
            else:
                raise ValueError(f"Invalid attribute '{attr}'")

        self._session.commit()
