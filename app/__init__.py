from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_required
from flask_bcrypt import Bcrypt
import git
import os

from app.config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = "users.login"
login_manager.login_message_category = "info"


def create_app(config_class=Config):
    """Create and configure the app"""
    app = Flask(__name__)
    app.config.from_object(Config)

    # initializing the flask extensions
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    from app.users.routes import users
    from app.receipt import receipts
    from app.util_routes import utils
    app.register_blueprint(users)
    app.register_blueprint(receipts)
    app.register_blueprint(utils)

    from app.models import Receipt

    # a simple page that says hello
    @app.route('/')
    def home():
        repo = git.Repo(os.path.join(__file__, "../.."))
        sha = repo.head.object.hexsha
        return render_template("index.html", commit_sha=sha)

    @app.route('/view')
    @login_required
    def view():
        return render_template("view.html", values=Receipt.query.all())

    return app
