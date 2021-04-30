from github_webhook import Webhook
from flask import Flask
from flask import request
import json

app = Flask(__name__)  # Standard Flask app
webhook = Webhook(app) # Defines '/postreceive' endpoint

@app.route("/")        # Standard Flask endpoint
def hello_world():
    return "Hello, World!"


@app.route("/payload")        # Standard Flask endpoint
def sipal():
    if request.method == 'POST':
        return "test"
    return "test /payload"

@webhook.hook()        # Defines a handler for the 'push' event
def on_push(data):
    print(data)
    print("Got push with: {}".format(data))
    return data


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)