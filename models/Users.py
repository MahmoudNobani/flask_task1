from conf import db


class User(db.Model):
    """this class represents the Users table
                Attributes:
                    id_ (primary key:int): represents the id of the unique user
                    first_name (string): represents the user first name
                    last_name (string): represents the user last name
                    age (int): represents the user age
                    gender (string): represents the user gender
                    PhoneNumbers : represents the relation between Users table and PhoneNumbers table
                    address : represents the relation between Users table and Address table
                """
    __tablename__ = "Users"
    id_ = db.Column(db.Integer, unique=True, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    age = db.Column(db.Integer)
    gender = db.Column(db.String(100))
    PhoneNumbers = db.relationship('PhoneNumbers', backref='Users', lazy=True, cascade="all, delete, delete-orphan")
    address = db.relationship('Address', backref="Users", lazy=True, cascade="all, delete, delete-orphan")

    def __init__(self, **kwargs):
        self.first_name = kwargs["first_name"]
        self.age = kwargs["age"]
        self.id_ = kwargs["id"]
        self.gender = kwargs["gender"]
        self.last_name = kwargs["last_name"]

    def update(self, **kwargs):
        """this function aims to update the Users object, thus the database
                        Args:
                            **kwargs: Arbitrary keyword arguments that represents the Users table main attribute,
                            relation not included
                        Returns:
                            no return value,
                                """
        self.first_name = kwargs["first_name"]
        self.age = kwargs["age"]
        self.id_ = kwargs["id"]
        self.gender = kwargs["gender"]
        self.last_name = kwargs["last_name"]

