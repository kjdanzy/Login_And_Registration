from flask_app.config.mysqlconnection import connectToMySQL, log_this
from flask_app import app

from flask import flash
import re
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at'] 
        self.updated_at = data['updated_at']

    @staticmethod
    def validate_login(data):
        is_valid = True # we assume this is true
        if len(data['first_name']) < 3:
            flash("The first name must be at least 3 characters.")
            is_valid = False
        if len(data['last_name']) < 3:
            flash("The last name must be at least 3 characters.")
            is_valid = False
        if len(data['email']) < 7:
            flash("Your email must be at least 7 characters.")
            is_valid = False
        if not EMAIL_REGEX.match(data['email']):
            flash("Your email address is not validly formed.  Please try again.  (i.e. somename@someplace.com [.edu, .gov, .com, etc.])")
            is_valid = False
        if len(data['password']) < 8:
            flash("Your password must be at least 8 characters.  Capeesh??")
            is_valid = False
        if not data['password'] == data['confirm_password']:
            flash("Your 'password' and 'confirm password' fields must match.")
            is_valid = False
        if is_valid:
            flash("We really like the way level-headed people like you fill out our forms!  \n:-) Please try your login now and have a great day!")
        return is_valid

    
    @classmethod
    def get_user_by_email(cls, data):
        query = "SELECT * FROM USERS WHERE EMAIL = %(email)s;"
        result = connectToMySQL("login_and_registration_schema").query_db(query, data)

        log_this("get_user_by_email", data, query, result)

        # didn't find a matching user
        if len(result) < 1:
            return False
        return cls(result[0])

    @classmethod
    def get_user_by_id(cls, data):
        query = "SELECT * FROM USERS WHERE ID = %(id)s;"
        result = connectToMySQL("login_and_registration_schema").query_db(query, data)

        log_this("get_user_by_id", data, query, result)
        
        # didn't find a matching user
        if len(result) < 1:
            return False
            
        return cls(result[0])

    # class method to save our user to the database
    @classmethod
    def save(cls, data ):
        print("===========")
        print(data)
        print("===========")
        query = "INSERT INTO USERS ( first_name, last_name, email, password, created_at ) VALUES ( %(first_name)s , %(last_name)s , %(email)s , %(password)s , NOW() );"
        print(query)
        print("===========")
        # data is a dictionary that will be passed into the save method from server.py
        return connectToMySQL('login_and_registration_schema').query_db( query, data )
