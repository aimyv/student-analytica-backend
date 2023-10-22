from flask import Blueprint, request, jsonify
from ..models.models import Result
from ..database.db import db
from werkzeug import exceptions
from sqlalchemy import update, select

results = Blueprint("results", __name__)


@results.route('/results', methods=['GET', 'POST'])
def all_results():
    if request.method == 'GET':
        results = Result.query.all()
        outputs = map(lambda r: {
            "id": r.id,
            "student_name": r.student_name, 
            "subject": r.subject,
            "score": r.score,
            "feedback": r.feedback
            }, results)
        usableOutputs = list(outputs)
        return jsonify(usableOutputs), 200
    elif request.method == 'POST':
        data = request.json
        new_result = Result(
            student_name=data["student_name"],
            subject=data["subject"],
            score=data["score"],
            feedback=data["feedback"],
            )
        db.session.add(new_result)
        db.session.commit()
        output = {
            "id": new_result.id, 
            "student_name": new_result.student_name,
            "subject": new_result.subject,
            "score": new_result.score,
            "feedback": new_result.feedback
            }
        return jsonify(output), 201

@results.route('/results/<int:result_id>', methods=['GET', 'DELETE'])
def results_handler(result_id):
    if request.method == 'GET':
        try:
            foundResult = Result.query.filter_by(id=result_id).first()
            output = {
                "id": foundResult.id,
                "student_name": foundResult.student_name,
                "subject": foundResult.subject,
                "score": foundResult.score,
                "feedback": foundResult.feedback,
            }
            return output
        except:
            raise exceptions.BadRequest(
                f"We do not have a result with that id: {result_id}")
    elif request.method == 'DELETE':
        try:
            foundResult = Result.query.filter_by(id=result_id).first()
            db.session.delete(foundResult)
            db.session.commit()
            return "deleted", 204
        except:
            raise exceptions.BadRequest(
                f"Failed to delete a result with that id: {result_id}")

@results.route('/results/<subject>', methods=['GET'])
def class_results_by_subject(subject):
    foundResults = Result.query.filter_by(subject=subject).all()
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
