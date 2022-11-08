import json
from flask import Flask, render_template, url_for, flash, redirect, request, jsonify

app = Flask(__name__)
global users_object_list


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


    def __init__(self, id, first_name, last_name, gender, age, address, phone_numbers):
        self.first_name = first_name
        self.age = age
        self.id = id
        self.phone_numbers = phone_numbers
        self.gender = gender
        self.last_name = last_name
        self.address = address

    def print_string(self) -> dict:
        """this function aims to print hte object and return its values as a dictionary
        Args:
            this function doesn't need any arguments

        Returns:
            returns dictionary d that represents the object attributes
                """
        print(self.id, self.first_name, self.last_name, self.age, self.gender, self.address, self.phone_numbers)
        d = {}
        d["id"] = self.id
        d["first_name"] = self.first_name
        d["last_name"] = self.last_name
        d["age"] = self.age
        d["gender"] = self.gender
        d["address"] = self.address
        d["phone_numbers"] = self.phone_numbers
        return d


def add_to_class(temp: object) -> bool:
    """this function aims to preserve the uniqueness of the id
            Args:
                temp: which represent the temp object of the user

            Returns:
                true if id is unique, false if not

            """
    for x in users_object_list:
        if temp.id is x.id:
            return False
    users_object_list.append(temp)
    return True


def print_json():
    """this function aims to print the edited changes onto the json file
        Args:
            this function doesn't need any arguments

        Returns:
            no return value

        """
    with open('temp.json', 'w') as f:
        x = []
        for i in users_object_list:
            d = i.print_string()
            x.append(d)
        json.dump(x, f)


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
        temp = User(i["id"], i["first_name"], i["last_name"], i["gender"], i["age"], i["address"], i["phone_numbers"])
        user_objects.append(temp)
    return user_objects


@app.route('/get_users', methods=['GET'])
def get_users() -> list:
    """this function perform a get method with the aim to return the users list

        Args:
            there is no parameters

        Returns:
            returns a list that contains all the user names we have plus a 201 status code

        """
    users_names = []
    if request.method == 'GET':
        user_counter = 1
        for i in users_object_list:
            temp = f"user " + str(user_counter) + ": " + i.first_name + " " + i.last_name + " " + str(i.id)
            users_names.append(temp)
            user_counter += 1
    return users_names, 201


@app.route('/get_user/<int:user_id>', methods=['GET'])
def get_user_with_id(user_id: int) -> dict:
    """this function Return the user with the given id.

        Args:
            user_id (int): represents the id of the user we want to search

        Returns:
            this function returns the data of the user with the given id

        """
    if request.method == 'GET':
        result = next((x for x in users_object_list if x.id == user_id), "no such user was found")
        if result == "no such user was found":
            return result, 201
        return result.print_string(), 201


@app.route('/add_user', methods=['POST'])
def add_user() -> json:
    """this function adds a new user to the users file
        Args:
            this function doesn't take any normal parameters, but takes some in the route

        Returns:
            returns a json of the data entered

        """
    if request.method == 'POST':
        new_user = request.json
        id = new_user['id']
        first_name = new_user['first_name']
        last_name = new_user['last_name']
        gender = new_user['gender']
        age = new_user['age']
        phone_numbers = new_user['phone_numbers']
        address = new_user['address']

        temp = User(int(id), first_name, last_name, gender, age, address, phone_numbers)
        unique = add_to_class(temp)
        if unique:
            print_json()
            return jsonify({'id': id, 'first_name': first_name, 'last_name': last_name, 'age': age, 'gender': gender,
                            'address': address, 'phone_numbers': phone_numbers}), 201
        else:
            del temp
            return "user id has to be unique", 201


@app.route('/del_user/<int:user_id>', methods=['DELETE'])
def del_user(user_id):
    """given the id, this function perform the delete operation on it

        Args:
             user_id (int): represents the id of the user we want to delete
        Returns:
            string: represents whether the operation was successful or not

        """
    if request.method == 'DELETE':
        for x in users_object_list:
            if x.id == user_id:
                users_object_list.remove(x)

                return "operation succesfull", 201
        return "user not found", 201


@app.route('/update_user/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """given the id, this function perform the delete operation on it

        Args:
             user_id (int): represents the id of the user we want to delete
        Returns:
            string: represents whether the operation was successful or not

        """
    if request.method == 'PUT':
        for x in users_object_list:
            if x.id == user_id:
                users_object_list.remove(x)
                updated_user = request.json
                first_name = updated_user['first_name']
                last_name = updated_user['last_name']
                gender = updated_user['gender']
                age = updated_user['age']
                phone_numbers = updated_user['phone_numbers']
                address = updated_user['address']
                temp = User(int(user_id), first_name, last_name, gender, age, address, phone_numbers)

                users_object_list.append(temp)
                print_json()
                return "operation succesfull", 201
        return "user not found", 201


if __name__ == '__main__':
    users_data = get_users_data()
    users_object_list = create_users_list(users_data)
    app.run(debug=True)
