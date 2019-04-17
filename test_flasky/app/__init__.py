from flask import Flask


app = Flask(__name__)

@app.route('/user/<name>')
def index(name):
    return f'{name}'

app.add_url_rule()