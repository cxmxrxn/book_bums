from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user

class Tutor:
    db_name = 'book_bums'
    def __init__(self,db_data):
        self.id = db_data['id']
        self.first_name = db_data['first_name']
        self.last_name = db_data['last_name']
        self.email = db_data['email']
        self.phone = db_data['phone']
        self.rate = db_data['rate']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']
        self.students = []
    
    @classmethod
    def save(cls,data):
        query = "INSERT INTO tutors (first_name,last_name,email,phone,rate) VALUES (%(first_name)s,%(last_name)s,%(email)s,%(phone)s,%(rate)s)"
        return connectToMySQL(cls.db_name).query_db(query,data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM tutors;"
        results = connectToMySQL(cls.db_name).query_db(query)
        all_tutors = []
        for tutor in results:
            print(tutor['id'])
            all_tutors.append(cls(tutor))
        return all_tutors
    @classmethod
    def destroy(cls,data):
        query = "DELETE FROM tutors WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)