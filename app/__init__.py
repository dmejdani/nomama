import os
from flask import Flask, request, abort, render_template
import json
import git
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

from utils import is_valid_signature
from app.config import Config

# env vars
wh_secret = os.getenv("WEBHOOK_SECRET")

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = "users.login"
login_manager.login_message_category = "info"


def create_app(config_class=Config):
    """Create and configure the app"""
    app = Flask(__name__)
    app.config.from_object(Config)

    # ensure the instance folder exists
    os.makedirs(app.instance_path, exist_ok=True)

    # initializing the flask extensions
    db.init_app(app)
    login_manager.init_app(app)

    from app import models

    # a simple page that says hello
    @app.route('/')
    @app.route('/hello')
    def home():
        return "hh"

    @app.route("/update-server", methods=["POST"])
    def webhook():
        if request.method == "POST":
            abort_code = 418
            # Do initial validations on required headers
            if 'X-Github-Event' not in request.headers:
                abort(abort_code)
            if 'X-Github-Delivery' not in request.headers:
                abort(abort_code)
            if 'X-Hub-Signature' not in request.headers:
                abort(abort_code)
            if not request.is_json:
                abort(abort_code)
            if 'User-Agent' not in request.headers:
                abort(abort_code)
            ua = request.headers.get('User-Agent')
            if not ua.startswith('GitHub-Hookshot/'):
                abort(abort_code)

            event = request.headers.get('X-GitHub-Event')
            if event == "ping":
                return json.dumps({'msg': 'Hi!'})
            # TODO: Event should be a pull request event
            if event != "push":
                return json.dumps({'msg': "Wrong event type"})

            x_hub_signature = request.headers.get("X-Hub-Signature")
            # webhook content type should be application/json for request.data to have the payload
            # request.data is empty in case of x-www-form-urlencoded
            if not is_valid_signature(x_hub_signature, request.data, wh_secret):
                print('Deploy signature failed: {sig}'.format(
                    sig=x_hub_signature))
                abort(abort_code)

            payload = request.get_json()
            if payload is None:
                print(f"Deploy payload is empty: {payload}")
                abort(abort_code)

            if payload["ref"] != "refs/heads/master":
                return json.dumps({"msg": "Not master; ignoring"})

            repo = git.Repo("~/nomama")
            origin = repo.remotes.origin

            pull_info = origin.pull()
            if len(pull_info) == 0:
                return json.dumps({'msg': "Didn't pull any information from remote!"})
            if pull_info[0].flags > 128:
                return json.dumps({'msg': "Didn't pull any information from remote!"})

            commit_hash = pull_info[0].commit.hexsha
            build_commit = f"build_commit = '{commit_hash}'"

            return f"Updated PythonAnywhere successfully to commit {build_commit}", 200
        return "Bad request", 400

    return app
