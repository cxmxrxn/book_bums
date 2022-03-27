from flask import render_template,redirect,session,request, flash
from flask_app import app
from flask_app.models.tutor import Tutor
from flask_app.models.student import Student
from flask_app.models.user import User

@app.route('/new/tutor')
def new_tutor_page():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":session['user_id']
    }
    return render_template('new_tutor.html',user=User.get_by_id(data))

@app.route('/create/tutor',methods=['POST'])
def create_tutor():
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
        "email": request.form['email'],
        "phone": request.form['phone'],
        "rate": request.form['rate']
    }
    Tutor.save(data)
    return redirect('/dashboard')

@app.route('/view/tutors')
def show_tutors():
    if 'user_id' not in session:
        return redirect('/logout')
    data ={
        'id': session['user_id']
    }
    return render_template("show_tutors.html",tutors=Tutor.get_all(),user=User.get_by_id(data),students=Student.get_all())

@app.route('/delete/tutor/<int:id>')
def delete_tutor(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data ={
        'id': id
    }
    Tutor.destroy(data)
    return redirect('/dashboard')