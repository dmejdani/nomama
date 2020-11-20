from flask import Blueprint, request, abort
import hashlib
import hmac
import json
import git
import os

# env vars
wh_secret = os.getenv("WEBHOOK_SECRET")

utils = Blueprint('utils', __name__)


def is_valid_signature(x_hub_signature, data, private_key):
    hash_algorithm, github_signature = x_hub_signature.split('=', 1)
    algorithm = hashlib.__dict__.get(hash_algorithm)
    encoded_key = bytes(private_key, 'latin-1')
    mac = hmac.new(encoded_key, msg=data, digestmod=algorithm)
    return hmac.compare_digest(mac.hexdigest(), github_signature)


@utils.route("/update-server", methods=["POST"])
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
