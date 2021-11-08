from flask_app import app
from flask_bcrypt import Bcrypt
from flask import render_template,redirect,request,session
from flask_app.config.mysqlconnection import MySQLConnection
from flask_app.models.user import User
bcrypt = Bcrypt(app)

# show all users
@app.route('/')
def all_users():
    users = User.get_all()
    print(users)
    return render_template("index.html", all_users = users)

# show one user without editing
@app.route('/user/<int:id>')
def showUser(id):
    data = {
        "id": id,
    }
    single_user = User.get_one(data)
    return render_template("one_user.html", single_user = single_user)

# show a single user and show the form
@app.route('/user/<int:id>/edit_page')
def show_edit_User(id):
    data = {
        "id": id,
    }
    single_user = User.get_one(data)
    return render_template("edit_user.html", single_user = single_user)

# edit a user saves the data to database
@app.route('/user/<int:id>/edit', methods=["POST"])
def editUser(id):
    data = {
        "id": id,
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email":request.form["email"],
        "password":request.form["password"],
    }
    User.edit_one(data)
    return redirect('/')

# create new user show form
@app.route('/create_new_user_page')
def create_new_user():
    return render_template("new.html")

# create new user save the data to database
@app.route('/create_new_user', methods=["POST"])
def create_user():
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["email"],
        "password":  pw_hash,
    }
    User.create_one(data)
    session["User"] = User
    return redirect('/')

@app.route('/log_in', methods=["POST"])
def login():
    # see if the username provided exists in the database
    data = { "email" : request.form["email"] }
    user_in_db = User.get_by_email(data)
    # user is not registered in the db
    if not user_in_db:
        flash("Invalid Email/Password")
        return redirect("/")
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        # if we get False after checking the password
        flash("Invalid Email/Password")
        return redirect('/')
    # if the passwords matched, we set the user_id into session
    session['user_id'] = user_in_db.id
    # never render on a post!!!
    return redirect("/success")

@app.route('/clear', methods=["POST"])
def clear():
    session.clear()
    return redirect("/")

@app.route('/delete/<int:id>', methods=["POST"])
def deleteUser(id):
    data = {
        "id":id
    }
    User.delete_one(data)
    return redirect('/')


