from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello():
    return "<h1>HELLO WORLD!</h1>"


@app.route('/api')
def api():
    return "<h1>THIS IS API</h1>"
