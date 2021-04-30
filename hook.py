from flask import Flask
from flask import request
import json

app = Flask(__name__)  # Standard Flask app

@app.route("/")        # Standard Flask endpoint
def hello_world():
    return "Github webhook"


@app.route("/payload", methods=['POST'])        # Standard Flask endpoint
def webhook_receiver():
    payload = request.get_json()  # dict object
    print(payload)
    print(type(payload))
    return "push received"



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)