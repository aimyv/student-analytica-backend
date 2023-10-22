from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from flask_cors import CORS
from .database.db import db
from .models.models import Teacher

def create_app():

    DB_NAME = 'database.db'

    app = Flask(__name__)
    CORS(app)
    app.config['SECRET_KEY'] = "helloworld"
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .routes.views import views
    from .routes.auth import auth
    from .routes.teachers import teachers
    from .routes.students import students
    from .routes.results import results

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(teachers, url_prefix='/')
    app.register_blueprint(students, url_prefix='/')
    app.register_blueprint(results, url_prefix='/')

    with app.app_context():
        db.create_all()
    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return Teacher.query.get(int(id))

    return app
