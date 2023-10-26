from flask import Blueprint, request, jsonify
from ..models.models import Student, Result
from ..database.db import db
from werkzeug import exceptions
from sqlalchemy import update, select, desc

students = Blueprint("students", __name__)

# view all students
# add a new student
@students.route('/students', methods=['GET', 'POST'])
def all_students():
    if request.method == 'GET':
        students = Student.query.all()
        outputs = map(lambda s: {
            "name": s.name
            }, students)
        usableOutputs = list(outputs)
        return jsonify(usableOutputs), 200
    elif request.method == 'POST':
        data = request.json
        new_student = Student(
            name=data["name"],
            results=[]
            )
        db.session.add(new_student)
        db.session.commit()
        output = {
            "name": new_student.name,
            "results": new_student.results}
        return jsonify(output), 201

# view a specific student
# delete a specific student
@students.route('/students/<student_name>', methods=['GET', 'DELETE'])
def students_handler(student_name):
    if request.method == 'GET':
        try:
            foundStudent = Student.query.filter_by(name=student_name).first()
            output = {
                "name": foundStudent.name
            }
            return output
        except:
            raise exceptions.BadRequest(
                f"We do not have a student with that name: {student_name}")
    elif request.method == 'DELETE':
        try:
            foundStudent = Student.query.filter_by(name=student_name).first()
            db.session.delete(foundStudent)
            db.session.commit()
            return "deleted", 204
        except:
            raise exceptions.BadRequest(
                f"Failed to delete a student with that name: {student_name}")

# view all results for a specific student
@students.route('/students/<student_name>/results', methods=['GET'])
def student_results(student_name):
    foundResults = Result.query.filter_by(student_name=student_name).all()
    outputs = map(lambda r: {
            "id": r.id,
            "student_name": r.student_name, 
            "subject": r.subject,
            "score": r.score,
            "feedback": r.feedback
            }, foundResults
        )
    usableOutputs = list(outputs)
    return jsonify(usableOutputs), 200

# view all results for a specific subject and student
@students.route('/students/<student_name>/results/<subject>', methods=['GET'])
def student_results_by_subject(student_name, subject):
    foundResults = Result.query.filter_by(student_name=student_name, subject=subject).all()
    outputs = map(lambda r: {
            "id": r.id,
            "student_name": r.student_name, 
            "subject": r.subject,
            "score": r.score,
            "feedback": r.feedback
            }, foundResults
        )
    usableOutputs = list(outputs)
    return jsonify(usableOutputs), 200
