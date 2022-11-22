from marshmallow import Schema, fields


class PhoneSchema(Schema):
    """this class the schema for the PhoneNumbers table
                    Attributes:
                        user_id (string): represents the id of the unique user
                        type (string): represents the phone type
                        number (string): represents the phone number
                    """
    user_id = fields.String()
    type = fields.String()
    number = fields.String()


class AddSchema(Schema):
    """this class the schema for the Address table
                        Attributes:
                            user_id (string): represents the id of the unique user
                            street_address (string): represents the street_address
                            city (string): represents the city
                            state (string): represents the state
                            postal_code (string): represents the postal_code
                        """
    user_id = fields.String()
    street_address = fields.String()
    city = fields.String()
    state = fields.String()
    postal_code = fields.String()


class UserSchema(Schema):
    """this class represents the Users table schema
                    Attributes:
                        id_ (string): represents the id of the unique user
                        first_name (string): represents the user first name
                        last_name (string): represents the user last name
                        age (string): represents the user age
                        gender (string): represents the user gender
                        PhoneNumbers : represents the relation between Users table and PhoneNumbers table
                        address : represents the relation between Users table and Address table
                    """
    id_ = fields.String()
    first_name = fields.String()
    last_name = fields.String()
    age = fields.String()
    gender = fields.String()
    address = fields.Nested(AddSchema(only=("street_address", "city", "state", "postal_code")), many=True)
    PhoneNumbers = fields.Nested(PhoneSchema(only=("type", "number")), many=True)

