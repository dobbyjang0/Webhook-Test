from flask import Flask
from flask import request
import json

app = Flask(__name__)  # Standard Flask app

class MetaSingleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(MetaSingleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class Descriptions(metaclass=MetaSingleton):
    def __init__(self):
        self.event_list = {
            'push': self._push,
            'issues': 0,
            'issue_comment': 0,
            'commit_comment': 0,
            'create': 0,
            'delete': 0,
            'pull_request': 0,
            'pull_request_review': 0,
            'pull_request_review_comment': 0,
            'fork': 0
        }

    def _push(self, context):
        commit_info = []
        commit_info.append(str(len(context['commits'])) + ' new commits')
        commit_info.append(context['compare'])
        for commit in context['commits']:
            commit_info.append(commit["id"][:4] + '-' + commit['message'] + ' by ' + commit['committer']['username'])

        result = '\n'.join(commit_info)
        return result




@app.route("/")        # Standard Flask endpoint
def hello_world():
    return "Github webhook"

@app.route("/payload", methods=['POST'])        # Standard Flask endpoint
def webhook_receiver():
    context = request.get_json()  # dict object
    event = request.headers.get('X-GitHub-Event')
    api_info = Descriptions()

    if event in api_info.event_list.keys():
        result = api_info.event_list[event](context)
    else:
        result = 'event receive'
    print(result)
    return result



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)