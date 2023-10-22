from flask import Blueprint, request, jsonify
from ..database.db import db
from ..models.models import Teacher
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug import exceptions

auth = Blueprint('auth', __name__)

@auth.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.json
        email = data['email']
        password = data['password']

        user = Teacher.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user, remember=True)
                return jsonify({"message": "Logged In.", "id": user.id, "username": user.username}), 201
            else:
                raise exceptions.BadRequest(f"Password is incorrect.")
        else:
            raise exceptions.NotFound(f"User doesn't exist.")
    else:
        raise exceptions.BadRequest(
            f"Send a POST request with the relevant attributes.")

@auth.route("/register", methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        data = request.json
        email = data['email']
        username = data['username']
        password1 = data['password1']
        password2 = data['password2']

        email_exists = Teacher.query.filter_by(email=email).first()
        username_exists = Teacher.query.filter_by(username=username).first()
        if email_exists:
            raise exceptions.BadRequest("Email is already in use.")
        elif username_exists:
            raise exceptions.BadRequest("Username is already in use.")
        elif password1 != password2:
            raise exceptions.BadRequest("Passwords don't match!")
        else:
            new_user = Teacher(
                email=email,
                username=username,
                password=generate_password_hash(password1, method='sha256')
                            )
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            return jsonify({"message": "User created!"}), 201
    else:
        raise exceptions.BadRequest(
            f"Send a POST request with the relevant attributes.")

@login_required
@auth.route("/logout")
def logout():
    logout_user()
    return jsonify({"message": "User logged out!"})
