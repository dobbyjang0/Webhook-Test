from github_webhook import Webhook
from flask import Flask

app = Flask(__name__)  # Standard Flask app
webhook = Webhook(app) # Defines '/postreceive' endpoint

@app.route("/", methods=['POST'])        # Standard Flask endpoint
def hello_world():
    return "Hello, World!"


@app.route("/payload", methods=['POST'])        # Standard Flask endpoint
def sipal():
    return "test /payload"

@webhook.hook()        # Defines a handler for the 'push' event
def on_push(data):
    print(data)
    print("Got push with: {}".format(data))
    return data


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=80)