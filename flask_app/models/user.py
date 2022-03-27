from flask_app.config.mysqlconnection import connectToMySQL
import re	# the regex module
# create a regular expression object that we'll use later   
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask import flash

class User:
    db_name = "book_bums"

    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save(cls,data):
        query = "INSERT INTO users (first_name,last_name,email,password) VALUES(%(first_name)s,%(last_name)s,%(email)s,%(password)s)"
        return connectToMySQL(cls.db_name).query_db(query,data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL(cls.db_name).query_db(query)
        users = []
        for row in results:
            users.append( cls(row))
        return users

    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        return cls(results[0])

    @staticmethod
    def validate_registration(form_input):
        is_valid = True # we assume this is true
        
        if len(form_input['first_name']) < 2:
            flash("First name must be at least 2 characters.", "register")
            is_valid = False

        if len(form_input['last_name']) < 2:
            flash("Last name must be at least 2 characters.", "register")
            is_valid = False

        if not EMAIL_REGEX.match(form_input['email']):
            flash("Invalid Email Address", "register")
            is_valid = False
        data = {
            "email": form_input["email"]
        }
        found_user_or_false = User.get_by_email(data)
        if found_user_or_false != False:
            is_valid = False
            flash("Email is already in use.", "register")
            
        if len(form_input['password']) < 8:
            flash("Your password must be at least 8 characters.", "register")
            is_valid = False
        
        if form_input['password'] != form_input['confirm']:
            flash("Passwords must be the same.", "register")
            is_valid = False

        return is_valid

    @staticmethod
    def validate_login(form_input):
        is_valid = True
        email_data = {
        "email": form_input["email"]
        }
        found_user_or_false = User.get_by_email(data)
        if found_user_or_false == False:
            is_valid = False
            flash("Invalid Login Credentials.", "login")
            return is_valid
        if not bcrypt.check_password_hash(found_user_or_false.password, form_input['password']):
            is_valid = False
            flash("Invalid Login Credentials.", "login")
        return is_valid