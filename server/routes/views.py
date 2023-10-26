from flask import Blueprint, request, jsonify
from werkzeug import exceptions
import openai
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

views = Blueprint('views', __name__)

openai.api_key_path = '.env'

@views.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@views.route("/report", methods=['POST'])
def report():
    message = request.json.get('message')
    completion = openai.ChatCompletion.create(
        model = 'gpt-3.5-turbo',
        messages=[
            {'role': 'user', 'content': message}
        ]
    )
    if completion.choices[0].message != None:
        return completion.choices[0].message
    else:
        return 'Failed to generate response!'
    # return f'{openai.api_key}'
