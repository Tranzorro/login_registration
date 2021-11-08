# import the function that will return an instance of a connection
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
# model the class after the users table from our database
class User:
    db = "login"
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    # Now we use class methods to query our database
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM Users;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        results = connectToMySQL(cls.db).query_db(query)
        # Create an empty list to append our instances of users
        users = []
        # Iterate over the db results and create instances of users with cls.
        for user in results:
            users.append( cls(user) )
        return users
    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM Users WHERE id = %(id)s;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        result = connectToMySQL(cls.db).query_db(query,data)
        # Iterate over the db results and create instances of users with cls.
        return cls(result[0])
    @classmethod
    def edit_one(cls, data):
        query = "UPDATE Users SET first_name = %(first_name)s, last_name = %(last_name)s, email = %(email)s WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def delete_one(cls, data):
        query = "DELETE FROM Users WHERE id = %(id)s;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def create_one(cls, data):
        query = "INSERT INTO Users ( first_name , last_name , email , created_at , updated_at ) VALUES ( %(first_name)s, %(last_name)s, %(email)s, NOW() , NOW() );"
        return connectToMySQL(cls.db).query_db( query,data)

    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM Users WHERE email = %(email)s;"
        result = connectToMySQL(cls.db).query_db(query,data)
        # Didn't find a matching user
        if len(result) < 1:
            return False
        return cls(result[0])


    @staticmethod
    def validate_user(user):
        is_valid = True
        # test whether a field matches the pattern
        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address!")
            is_valid = False
        return is_valid

    @staticmethod
    def validate_register(form_data):
        is_valid = True
        if len(form_data['first_name']) < 3:
            flash("first name must be at least 3 characters.")
            is_valid = False
        if len(form_data['last_name']) < 3:
            flash("last name must be at least 3 characters.")
            is_valid = False
        if len(form_data['email']) < 3:
            flash("must be a valid email address")
            is_valid = False
        if len(form_data['password']) < 16:
            flash("password must be at least 16 characters.")
            is_valid = False
        return is_valid