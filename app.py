from flask import Flask
from pathlib import Path
from flask_login import LoginManager

from models.database import db
from models.user import User
from models.subject import Subject
from models.task import Task

from routes.auth import auth
from routes.dashboard import dashboard
from routes.subjects import subjects

from routes.tasks import tasks

import os

app = Flask(__name__)

BASE_DIR = Path(__file__).resolve().parent

app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"sqlite:///{BASE_DIR / 'instance' / 'study_manager.db'}"
)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "auth.login"

app.register_blueprint(auth)
app.register_blueprint(dashboard)
app.register_blueprint(subjects)
app.register_blueprint(tasks)




@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/")
def home():
    return "Student Study Manager is running!"


with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(debug=True, port=8000)