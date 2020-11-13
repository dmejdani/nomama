from flask import Flask, request
import git

app = Flask(__name__)


@app.route("/")
def index():
    return "Index Page"


@app.route("/hello")
def hello():
    return "Hello, World!"

@app.route("/update-server", methods=["POST"])
def webhook():
    if request.method == "POST":
        repo = git.Repo("~/nomama")
        origin = repo.remotes.origin
        origin.pull()

        return "Updated PythonAnywhere successfully", 200
    return "Bad request", 400
