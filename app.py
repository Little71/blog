from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/')
def index():
    username = request.form['username']
    password = request.form['password']

    if username == "root" and password == "123456":
        return jsonify({'state': True,'msg':'登录成功'}),'200 ok'
    return jsonify({'state':False,'msg':'用户名密码错误'}),'403'


if __name__ == '__main__':
    app.run()
