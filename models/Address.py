from sqlalchemy import ForeignKey

from conf import db


class Address(db.Model):
    """this class represents the address table (multi-values attribute)
            Attributes:
                user_id (primary key:int): represents the id of the user that lives in that address,
                the user_id is the foreign key directly connected to users table
                street_address (string): represents the street address
                city (string): represents the city
                state (string): represents the state
                postal_code (string): represents the postal_code
            """
    __tablename__ = "Address"
    user_id = db.Column(db.Integer, ForeignKey("Users.id_", ondelete='CASCADE'), primary_key=True)
    street_address = db.Column(db.String(100))
    city = db.Column(db.String(100))
    state = db.Column(db.String(100))
    postal_code = db.Column(db.String(100))

    def __init__(self, id_, **kwargs):
        self.user_id = id_
        self.street_address = kwargs["street_address"]
        self.city = kwargs["city"]
        self.state = kwargs["state"]
        self.postal_code = kwargs["postal_code"]

    def update(self, id_, **kwargs):
        """this function aims to update the address object, thus the database
                Args:
                    id_ (int): represents the id of the user.
                    **kwargs: Arbitrary keyword arguments that represents the address table attribute
                Returns:
                    no return value
                        """
        self.user_id = id_
        self.street_address = kwargs["street_address"]
        self.city = kwargs["city"]
        self.state = kwargs["state"]
        self.postal_code = kwargs["postal_code"]
