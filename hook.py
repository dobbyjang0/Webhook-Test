from github_webhook import Webhook
from flask import Flask

app = Flask("project alert")  # Standard Flask app
webhook = Webhook(app) # Defines '/postreceive' endpoint

@app.route("/")        # Standard Flask endpoint
def hello_world():
    return "Hello, World!"


@app.route("/payload")        # Standard Flask endpoint
def sipal():
    return "Hello, World!"

@webhook.hook()        # Defines a handler for the 'push' event
def on_push(data):
    print(data)
    print("Got push with: {}".format(data))


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=80)