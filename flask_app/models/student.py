from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user
from flask_app.models import tutor

class Student:
    db_name = 'book_bums'
    def __init__(self,db_data):
        self.id = db_data['id']
        self.first_name = db_data['first_name']
        self.last_name = db_data['last_name']
        self.parent_name = db_data['parent_name']
        self.email = db_data['email']
        self.phone = db_data['phone']
        self.appointment = db_data['appointment']
        self.tutor_id = db_data['tutor_id']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']
        self.tutor_id = db_data['tutor_id']
        self.tutor = None
    
    @classmethod
    def save(cls,data):
        query = "INSERT INTO students (first_name,last_name,parent_name,email,phone,appointment,tutor_id) VALUES (%(first_name)s,%(last_name)s,%(parent_name)s,%(email)s,%(phone)s,%(appointment)s,%(tutor_id)s);"
        return connectToMySQL(cls.db_name).query_db(query,data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM students ORDER BY last_name ASC;"
        results = connectToMySQL(cls.db_name).query_db(query)
        all_students = []
        for student in results:
            print(student['id'])
            all_students.append(cls(student))
        return all_students
    
    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM students WHERE id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        return cls(results[0])
    
    @classmethod
    def destroy(cls,data):
        query = "DELETE FROM students WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)

    @classmethod
    def update(cls,data):
        query = "UPDATE students SET first_name=%(first_name)s,last_name=%(last_name)s,parent_name=%(parent_name)s,email=%(email)s,phone=%(phone)s,appointment=%(appointment)s,tutor_id=%(tutor_id)s WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)
    
    @classmethod
    def get_all_with_tutors(cls):
        query = "SELECT * FROM students JOIN tutors ON tutors.id = students.tutor_id;"
        results = connectToMySQL(cls.db_name).query_db(query)
        students_with_tutor = []
        for row in results:
            one_student = cls(row)
            one_students_tutor = {
                "id": row["tutors.id"],
                "first_name": row["tutors.first_name"],
                "last_name": row["tutors.last_name"],
                "email": row["tutors.email"],
                "phone": row["tutors.phone"],
                "rate": row["rate"],
                "created_at": row["tutors.created_at"],
                "updated_at": row["tutors.updated_at"]
            }
            my_tutor = tutor.Tutor(one_students_tutor)
            one_student.tutor = my_tutor
            students_with_tutor.append(one_student)
        return students_with_tutor