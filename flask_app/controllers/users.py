from flask_app import app
from flask import flash
from flask_bcrypt import Bcrypt
from flask import render_template,redirect,request,session
from flask_app.config.mysqlconnection import MySQLConnection
from flask_app.models.user import User
bcrypt = Bcrypt(app)

# show all users
@app.route('/')
def all_users():
    return render_template("index.html")

@app.route('/success')
def success():
    data = {
        "id": session["user_id"]
    }
    this_user = User.get_one(data)
    if 'user_id' in session:
        return render_template("/success.html", this_user = this_user)
# show one user without editing
# @app.route('/user/<int:id>')
# def showUser(id):
#     data = {
#         "id": id,
#     }
#     single_user = User.get_one(data)
#     return render_template("one_user.html", single_user = single_user)

# show a single user and show the form
# @app.route('/user/<int:id>/edit_page')
# def show_edit_User(id):
#     data = {
#         "id": id,
#     }
#     single_user = User.get_one(data)
#     return render_template("edit_user.html", single_user = single_user)

# edit a user saves the data to database
# @app.route('/user/<int:id>/edit', methods=["POST"])
# def editUser(id):
#     data = {
#         "id": id,
#         "first_name": request.form["first_name"],
#         "last_name": request.form["last_name"],
#         "email":request.form["email"],
#         "password":request.form["password"],
#     }
#     User.edit_one(data)
#     return redirect('/')

# create new user show form
# @app.route('/create_new_user_page')
# def create_new_user():
#     return redirect("/")

# create new user save the data to database
@app.route('/create_new_user', methods=["POST"])
def create_user():
    if not User.validate_register(request.form):
        return redirect("/")
    data = {
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["email"],
        "password":  bcrypt.generate_password_hash(request.form['password']),
    }
    session['user_id'] = User.create_one(data)
    return redirect('/success')

@app.route('/log_in', methods=["POST"])
def login():
    data = { 
        "email" : request.form["email"]
        }
    acceptable_id = User.validate_user(request.form, data)
    if acceptable_id == False:
        return redirect("/")
    session['user_id'] = acceptable_id
    return redirect("/success")

@app.route('/logout')
def logout():
    session.clear()
    return redirect("/")

@app.route('/delete/<int:id>', methods=["POST"])
def deleteUser(id):
    data = {
        "id":id
    }
    User.delete_one(data)
    return redirect('/')


