from flask import Blueprint, request, jsonify
from werkzeug import exceptions
import openai
from dotenv import load_dotenv, find_dotenv

# finds api key from .env file and loads it in
load_dotenv(find_dotenv())
openai.api_key_path = '.env'

views = Blueprint('views', __name__)

@views.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

# sends student feedback to openai
# response is a list of study strategies based on student feedback
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
