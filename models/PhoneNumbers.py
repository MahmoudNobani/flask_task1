from sqlalchemy import ForeignKey

from conf import db


class PhoneNumbers(db.Model):
    """this class represents the phone numbers table (multi-values attribute)
                Attributes:
                    user_id (int): represents the id of the user who uses that number,
                    the user_id is the foreign key directly connected to users table
                    type (string): represents the type of number used
                    number (primary key:string): represents the number itself, and its a unique one
                """

    __tablename__ = "phone_numbers"
    user_id = db.Column(db.Integer, ForeignKey("Users.id_", ondelete='CASCADE'), nullable=False)
    type = db.Column(db.String(100))
    number = db.Column(db.String(100), primary_key=True)

    def __init__(self, id_, **kwargs):
        self.user_id = id_
        self.type = kwargs["type"]
        self.number = kwargs["number"]