from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from ..models.models import Teacher
from ..database.db import db
from werkzeug import exceptions
from sqlalchemy import update, select

teachers = Blueprint("teachers", __name__)

# view all teachers registered to student analytica portal
@teachers.route('/teachers')
def all_teachers():
    teachers = Teacher.query.all()
    outputs = map(lambda t: {
        "id": t.id, 
        "email": t.email, 
        "username": t.username, 
        "password": t.password
        }, teachers)
    usableOutputs = list(outputs)
    return jsonify(usableOutputs), 200
