from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.signin import Signin
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/success')
def success():
    return render_template('success.html')

@app.route('/createUser', methods=['post'])
def createUser():
    data = {
        "fName": request.form["fName"],
        "lName": request.form["lName"],
        "email": request.form["email"],
        "password": request.form["password"],
        "cPass": request.form["cPass"]
    }
    if not Signin.validate_signup(data):
        return redirect('/')
    
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data['password'] = pw_hash
    session['nid'] = {
        "users_id": Signin.get_id_by_email(data),
        "first_name": Signin.get_first_name_by_id(Signin.get_id_by_email(data)[0])
    }
    Signin.create(data)
    return redirect('/success')

@app.route('/login', methods=['post'])
def login():
    data = {
        "email": request.form["email"],
        "password": request.form["password"]
    }
    if not Signin.validate_login(data):
        return redirect('/')
    session['nid'] = {
        "users_id": Signin.get_id_by_email(data),
        "first_name": Signin.get_first_name_by_id(Signin.get_id_by_email(data)[0])
    }
    print(session['nid'])
    return redirect('/success')

@app.route('/logout', methods=['post'])
def logout():
    session.pop("nid")
    
    return redirect('/')
