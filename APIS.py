import json
import string

from flask import request, jsonify



class User:
    """this class represents the user

        Attributes:
            id (int): represents the id of the user
            first_name (string): represents the first name of the user
            last_name (string): represents the last name of the user
            gender (string): represents the gender of the user
            age (string): represents the age of the user
            address (string): represents the address of the user
            phone_numbers (string): represents the phone_number of the user

        """

    def __init__(self, **kwargs):
        self.first_name = kwargs["first_name"]
        self.age = kwargs["age"]
        self.id_ = kwargs["id"]
        self.phone_numbers = kwargs["phone_numbers"]
        self.gender = kwargs["gender"]
        self.last_name = kwargs["last_name"]
        self.address = kwargs["address"]

    def print_string(self) -> dict:
        """this function aims to print hte object and return its values as a dictionary
        Args:
            this function doesn't need any arguments

        Returns:
            returns dictionary d that represents the object attributes
                """
        print(self.id_, self.first_name, self.last_name, self.age, self.gender, self.address, self.phone_numbers)

        dict_user = {"id": self.id_, "first_name": self.first_name, "last_name": self.last_name, "age": self.age,
                     "gender": self.gender, "address": self.address, "phone_numbers": self.phone_numbers}
        # print(dict_user)
        return dict_user


def start():
    """this function aims to start the program and get the necessary data we need like the list of users
                Args:
                    no args

                Returns:
                    no return value

                """
    global users_object_list
    users_data = get_users_data()
    users_object_list = create_users_list(users_data)


def add_to_class(temp: object) -> bool:
    """this function aims to preserve the uniqueness of the id
            Args:
                temp: which represent the temp object of the user

            Returns:
                true if id is unique, false if not

            """
    for x in users_object_list:
        if temp.id_ == x.id_:
            return False
    users_object_list.append(temp)
    return True


def get_users_data() -> dict:
    """ the function aime to read the data from the input file
    Args:
        this function doesn't need any arguments
    Returns:
        The return value is a dictionary of the input data
    """

    with open('users.json') as f:
        users_temp = json.load(f)
    return users_temp


def create_users_list(users_data: dict) -> list:
    """ the function aime to create a list of objects for each user from the input file
    Args:
        users_data (dict): represent the input data
    Returns:
        The return value is a list of the input objects
    """
    user_objects = []
    for i in users_data:
        temp = User(**i)
        # temp = User(i["id"], i["first_name"], i["last_name"], i["gender"], i["age"], i["address"], i["phone_numbers"])
        user_objects.append(temp)
    return user_objects


def get_user_with_id(user_id: string) -> json:
    """this function Return the user with the given id_.

        Args:
            user_id (string): represents the id_ of the user we want to search

        Returns:
            this function returns the data of the user with the given id_ as a dict

        """
    print(user_id)
    result = next((x for x in users_object_list if x.id_ == int(user_id)), "no such user was found")
    if result == "no such user was found":
        return jsonify(result),404
    return jsonify(result.print_string()),200


def del_user(user_id: string) -> json:
    """given the id, this function perform the delete operation on it

        Args:
             user_id (string): represents the id of the user we want to delete
        Returns:
            string: represents whether the operation was successful or not

        """

    for x in users_object_list:
        if x.id_ == int(user_id):
            users_object_list.remove(x)
            return jsonify("operation was successful"),202
    return jsonify("user not found"),404


def update_user(user_id: string) -> json:
    """given the id, this function perform the update operation on it

        Args:
             user_id (string): represents the id of the user we want to update
        Returns:
            string: represents whether the operation was successful or not

        """

    for x in users_object_list:
        print(x.id_, " ", user_id)
        if x.id_ == int(user_id):
            users_object_list.remove(x)
            updated_user = request.json
            updated_user["id"] = int(user_id)
            temp = User(**updated_user)
            users_object_list.append(temp)
            return jsonify("operation successful"),201
    return jsonify("user not found"),404


def get_users() -> json:
    """this function perform a get method with the aim to return the users list

        Args:
            there is no parameters

        Returns:
            returns a list that contains all the user names we have

        """
    """another approach
    users_names = []
    user_counter = 1
    for i in users_object_list:
        temp = f"user " + str(user_counter) + ": " + i.first_name + " " + i.last_name + " " + str(i.id_)
        users_names.append(temp)
        user_counter += 1
    return users_names"""


    all_users_data = []
    for i in users_object_list:
        data = i.print_string()
        all_users_data.append(data)
    return jsonify(all_users_data),200


def add_user() -> json:
    """this function adds a new user to the users file
        Args:
            this function doesn't take any normal parameters

        Returns:
            returns a json of the data entered

        """
    new_user = request.json
    temp = User(**new_user)
    unique = add_to_class(temp)
    if unique:
        return jsonify(new_user),201
    else:
        del temp
        return jsonify("user id has to be unique"),404
