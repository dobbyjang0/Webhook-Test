from flask import Flask
from flask import request
import json


class EventHandler:
    def __init__(self):
        self.event_list = {
            'push': self._push,   # test ok
            'issues': self._issues,   # test ok
            'issue_comment': self._issue_comment,   # test ok
            'commit_comment': self._commit_comment,   # test ok
            'create': self._create,   # test ok
            'delete': self._delete,   # test ok
            'pull_request': self._pull_request,   # No test
            'pull_request_review': self._pull_request_review,   # No test
            'pull_request_review_comment': self._pull_request_review_comment,   # No test
            'fork': self._fork   # No test
        }

    def _push(self, context):
        commit_info = []
        commit_info.append(context['compare'])
        if len(context['commits']) == 0:
            return '0'
        commit_info.append(str(len(context['commits'])) + ' new commits')
        for commit in context['commits']:
            commit_info.append(
                commit["id"][:6] + '-' + commit['message'] + ' by ' + commit['committer']['username']
            )
        result = '\n'.join(commit_info)
        return result

    def _issues(self, context):
        commit_info = []
        commit_info.append(context['issue']['html_url'])
        commit_info.append(
            'Issue ' + context['action'] + ' #' + str(context['issue']['number']) + ': ' + context['issue']['title']
        )
        result = '\n'.join(commit_info)
        return result

    def _issue_comment(self, context):
        commit_info = []
        commit_info.append(context['issue']['html_url'])
        commit_info.append(
            'Comment ' + context['action'] + ' on issue #' + str(context['issue']['number'])
        )
        result = '\n'.join(commit_info)
        return result

    def _commit_comment(self, context):
        commit_info = []
        commit_info.append(context['comment']['html_url'])
        commit_info.append(
            'Comment ' + context['action'] + ' on commit ' + str(context['comment']['commit_id'][:6])
        )
        result = '\n'.join(commit_info)
        return result

    def _create(self, context):
        commit_info = []
        commit_info.append(context['repository']['html_url'])
        commit_info.append(
            'Created ' + context['ref_type'] + ': ' + context['ref']
        )
        result = '\n'.join(commit_info)
        return result

    def _delete(self, context):
        commit_info = []
        commit_info.append(context['repository']['html_url'])
        commit_info.append(
            'Deleted ' + context['ref_type'] + ': ' + context['ref']
        )
        result = '\n'.join(commit_info)
        return result

    def _pull_request(self, context):
        commit_info = []
        commit_info.append(context['pull_request']['html_url'])
        if context['action'] == 'closed' and context['pull_request']['merged'] == False:
            context['action'] = 'closed and not merged'
        elif context['action'] == 'closed' and context['pull_request']['merged'] == True:
            context['action'] = 'merged'
        commit_info.append(
            'Pull request ' + context['action'] + ' #' + str(context['number']) + ': ' + context['pull_request']['title']
        )
        commit_info.append(context['pull_request']['body'])
        result = '\n'.join(commit_info)
        return result

    def _pull_request_review(self, context):
        commit_info = []
        commit_info.append(context['review']['html_url'])
        commit_info.append(
            'Pull request review ' + context['action'] + ' on pull request #' + str(context['pull_request']['number'])
        )
        result = '\n'.join(commit_info)
        return result

    def _pull_request_review_comment(self, context):
        commit_info = []
        commit_info.append(context['comment']['html_url'])
        commit_info.append(
            'Pull request review comment' + context['action'] + ' on pull request #' + str(context['pull_request']['number'])
        )
        result = '\n'.join(commit_info)
        return result

    def _fork(self, context):
        commit_info = []
        commit_info.append(context['forkee']['html_url'])
        commit_info.append(
            'Fork created: ' + context['forkee']['full_name']
        )
        result = '\n'.join(commit_info)
        return result


# Flask app
app = Flask(__name__)

# Flask endpoint
@app.route("/")
def hello_world():
    return "Github webhook"

# Flask endpoint
@app.route("/payload", methods=['POST'])
def webhook_receiver():
    context = request.get_json()  # dict object
    event = request.headers.get('X-GitHub-Event')
    api_info = EventHandler()

    if event in api_info.event_list.keys():
        result = api_info.event_list[event](context)
    else:
        result = 'success'
    print(result)
    return result

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)