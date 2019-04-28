from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/index',methods=['POST','GET'])
def index():
    username = request.form.get('username')
    password = request.form.get('password')

    print(username,password)

    if username == "root" and password == "123456":
        return jsonify({'state': True,'msg':'登录成功'}),'200 ok'
    return jsonify({'state':False,'msg':'用户名密码错误'}),'404'



if __name__ == '__main__':
    app.run()
