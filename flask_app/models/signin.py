from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import app
import re
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

# model the class after the friend table from our database
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
class Signin:
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    # Now we use class methods to query our database
    @staticmethod
    def validate_signup(signup):
        valid = True
        if len(signup['fName']) < 2:
            flash("First name must be at least 2 characters.")
            valid = False
        if len(signup['lName']) < 2:
            flash("Last name must be at least 2 characters.")
            valid = False
        if not EMAIL_REGEX.match(signup['email']):
            flash("Invalid email address.")
            valid = False
        if len(signup['password']) < 8:
            flash("Password must be at least 8 characters.")
            valid = False
        if signup['password'] == signup['cPass']:
            flash("Passwords must match")
            valid = False
        return valid

    @staticmethod
    def validate_login(login):
        valid = True
        id = Signin.get_id_by_email(login)
        print(id)
        if len(id) == 0:
            flash('Email/Password do not match any in our records')
            valid = False
        else:
            data = {
                "id": Signin.get_id_by_email(login)[0]
            }
            password = Signin.get_password_by_id(data['id'])
            print(password[0]['password'])
            if not bcrypt.check_password_hash(password[0]['password'], login['password']):
                flash('Email/Password do not match any in our records')
                valid = False
        return valid

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM signins;"
        results = connectToMySQL('signin_schema').query_db(query)
        users = []
        for user in results:
            users.append( cls(user) )
        return users

    @classmethod
    def create(cls, data):
        query = "INSERT INTO signins ( first_name , last_name , email, password, created_at, updated_at) VALUES ( %(fName)s, %(lName)s, %(email)s, %(password)s, NOW(), NOW());"
        return connectToMySQL('signin_schema').query_db( query, data )

    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM signins WHERE email = %(email)s;"
        return connectToMySQL('signin_schema').query_db( query, data)

    @classmethod
    def get_id_by_email(cls, data):
        query = "SELECT id FROM signins WHERE email = %(email)s;"
        return connectToMySQL('signin_schema').query_db( query, data)

    @classmethod
    def get_password_by_id(cls, data):
        query = "SELECT password FROM users WHERE id = %(id)s;"
        return connectToMySQL('mypies_schema').query_db( query, data)