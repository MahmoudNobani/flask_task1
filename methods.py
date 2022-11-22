import itertools
import json
import string

from flask import jsonify, request

from conf import db
from models.Address import Address
from models.PhoneNumbers import PhoneNumbers
from models.Users import User
from schema import UserSchema


def add_user_gen(data: json) -> string:
    """ the function aims to add a new user to the database
        Args:
            data (json): json representation fo the new user we want to add
        Returns:
            The return value is a string that either represent the success or failure of the addition process
    """
    n = 5  # length of smaller half
    updated_user_data = iter(data.items())  # put the items of updated users in an iterable

    user_data = dict(itertools.islice(updated_user_data, n))  # list of user date: id,fname,lname,gender,age
    remaining_data = dict(updated_user_data)  # grab the rest of the data (address, phone)
    remaining_data_items = iter(remaining_data.items())  # put the items of the remaining data in iterable

    address_data = dict(itertools.islice(remaining_data_items, 1))  # list of address only
    phone_data = dict(remaining_data_items)  # list of phone only

    # add to the user object
    new_user = User(**user_data)
    temp = Address(user_data["id"], **address_data["address"])
    new_user.address.append(temp)

    for i in phone_data["phone_numbers"]:
        temp = PhoneNumbers(user_data["id"], **i)
        new_user.PhoneNumbers.append(temp)

    try:
        db.session.add(new_user)
        db.session.commit()
        return str(new_user.id_)
    except Exception as err:
        return "unique constrains in user id and phone failed to be applied, " + f"Unexpected {err=}, {type(err)=}"


def get_all_users() -> json:
    """this function perform a get method with the aim to return all the users

        Args:
            there is no parameters

        Returns:
            returns a json that contains all the users we have, with 200 status code

        """
    people = User.query.all()
    schema = UserSchema(many=True)
    return jsonify(schema.dump(people)), 200


def add_user() -> json:
    """this function adds a new user to teh database with the help of add_user_gen
        Args:
            this function doesn't take any parameters

        Returns:
            returns the new user data as a json on success with 201 status code or
            an error message as a json representing what went wrong with 400 status code

        """
    new_user = request.json
    validation = add_user_gen(new_user)
    print(validation)
    if validation[:6] == "unique":
        return jsonify(validation), 400
    new_user_data = User.query.filter(int(validation) == User.id_)
    schema = UserSchema(many=True)
    return jsonify(schema.dump(new_user_data)), 201


def get_user_with_id(user_id: string) -> json:
    """this function Return the user with the given id_.

        Args:
            user_id (string): represents the id_ of the user we want to search

        Returns:
            this function returns the data of the user with the given id_ as a json wih 200 status code
            or an error message

        """
    try:
        people = User.query.filter(int(user_id) == User.id_)
        schema = UserSchema(many=True)
        if not schema.dump(people):
            return jsonify("user was not found"), 404
        return schema.dump(people), 200
    except Exception as err:
        return jsonify("entered id has to be integer, " + f"Unexpected {err=}, {type(err)=}"), 400


def del_user(user_id: string) -> json:
    """given the id, this function perform the delete operation on it

        Args:
             user_id (string): represents the id of the user we want to delete
        Returns:
            a json that represents whether the operation was successful or not
            or an error message representing what went wrong

        """

    try:
        deleted_users = User.query.filter(int(user_id) == User.id_).delete()
        PhoneNumbers.query.filter(int(user_id) == PhoneNumbers.user_id).delete()
        Address.query.filter(int(user_id) == Address.user_id).delete()
        if deleted_users > 0:
            db.session.commit()
            return jsonify("delete was successful"), 202
        else:
            return jsonify("user not found"), 404
    except Exception as err:
        return jsonify("entered id has to be integer, " + f"Unexpected {err=}, {type(err)=}"), 400


def update_user(user_id: string) -> json:
    """given the id, this function perform the update operation on it with the help of
    update_user_gen function

        Args:
             user_id (string): represents the id of the user we want to update
        Returns:
            json message that represents whether the operation was successful or not

        """
    updated_user = request.json
    updated_user["id"] = int(user_id)
    try:
        user = db.session.execute(db.select(User).filter(User.id_ == int(user_id))).one()
    except Exception as err:
        return jsonify(f"Unexpected {err=}, {type(err)=}"), 404

    update_user_gen(user, updated_user)
    db.session.commit()
    return jsonify("update successful"), 201


def update_user_gen(user: object, updated_user: json) -> json:
    """ the function aims to update the user object
            Args:
                user (object): represents the user we want to update
                updated_user (json): json representation of the updated information
            Returns:
                    there is no return value
                        """

    n = 5  # length of smaller half
    updated_user_data = iter(updated_user.items())  # put the items of updated users in an iterable

    user_data = dict(itertools.islice(updated_user_data, n))  # list of user date: id,fname,lname,gender,age
    remaining_data = dict(updated_user_data)  # grab the rest of the data (address, phone)
    remaining_data_items = iter(remaining_data.items())  # put the items of the remaining data in iterable

    address_data = dict(itertools.islice(remaining_data_items, 1))  # list of address only
    phone_data = dict(remaining_data_items)  # list of phone only
    # update user date
    user[0].update(**user_data)
    # update the phone numbers data
    user[0].PhoneNumbers.clear()
    for i in phone_data["phone_numbers"]:
        temp2 = PhoneNumbers(user_data["id"], **i)
        user[0].PhoneNumbers.append(temp2)
    # update the address data
    user[0].address[0].update(user_data["id"], **address_data["address"])
