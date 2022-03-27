from flask import render_template,redirect,session,request, flash
from flask_app import app
from flask_app.models.tutor import Tutor
from flask_app.models.student import Student
from flask_app.models.user import User

@app.route('/new/student')
def new_student_page():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":session['user_id']
    }
    return render_template('new_student.html',user=User.get_by_id(data),tutors=Tutor.get_all())

@app.route('/create/student',methods=['POST'])
def create_student():
    if 'user_id' not in session:
        return redirect('/logout')
#    if not Tutor.validate_tutor(request.form):
#        return redirect('/new/tutor')
    data = {
        "id":session['user_id']
    }
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "parent_name": request.form['parent_name'],
        "email": request.form['email'],
        "phone": request.form['phone'],
        "appointment": request.form['appointment'],
        "tutor_id": request.form['tutor_id']
    }
    Student.save(data)
    return redirect('/dashboard')

@app.route('/view/students')
def show_students():
    if 'user_id' not in session:
        return redirect('/logout')
    data ={
        'id': session['user_id']
    }
    return render_template("show_students.html",tutors=Tutor.get_all(),user=User.get_by_id(data),students=Student.get_all(),data=Student.get_all_with_tutors())

@app.route('/edit/student/<int:id>')
def edit_student(id):
    if 'user_id' not in session:
        return redirect('/logout')
#    if not Tutor.validate_tutor(request.form):
#        return redirect('/new/tutor')
    data ={
        'id': id
    }
    return render_template("edit_student.html", student=Student.get_by_id(data),tutors=Tutor.get_all(), data=Student.get_all_with_tutors())

@app.route('/update/student',methods=['POST'])
def update_student():
    if 'user_id' not in session:
        return redirect('/logout')
#    if not Tutor.validate_tutor(request.form):
#        return redirect('/new/tutor')
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "parent_name": request.form['parent_name'],
        "email": request.form['email'],
        "phone": request.form['phone'],
        "appointment": request.form['appointment'],
        "tutor_id": request.form['tutor_id'],
        "id": request.form['id']
    }
    Student.update(data)
    return redirect('/view/students')

@app.route('/delete/student/<int:id>')
def delete_student(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data ={
        'id': id
    }
    Student.destroy(data)
    return redirect('/dashboard')

@app.route('/check_out/<int:id>')
def check_out(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data ={
        'id': id
    }
    return render_template("check_out.html", student=Student.get_by_id(data),tutors=Tutor.get_all(), data=Student.get_all_with_tutors())

@app.route('/checked_out')
def checked_out():
    if 'user_id' not in session:
        return redirect('/logout')
#   if not Tutor.validate_tutor(request.form):
#        return redirect('/new/tutor')
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "parent_name": request.form['parent_name'],
        "email": request.form['email'],
        "phone": request.form['phone'],
        "appointment": request.form['appointment'],
        "tutor_id": request.form['tutor_id'],
        "id": request.form['id']
    }
    Student.check_out(data)
    return redirect('/dashboard')