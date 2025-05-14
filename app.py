from flask import Flask
from flask.wrappers import Response

app = Flask(__name__)

@app.route("/")
def hello_world():
  return Response("Hello World!")