from flask import Flask, request, jsonify
from flask_restful import Resource, reqparse
from queue_user_login import insert_user_in_logs
from flask_restful import Api

users = {
    'maria': 'password1',
    'user2': 'password2'
}

class Userlogin(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, required=True, help='username is required')
        parser.add_argument('password', type=str, required=True, help='password is required')
        parser.add_argument('code', type=str, required=True, help='code is required')
        args = parser.parse_args()
        username = args['username']
        password = args['password']
        code = args['code']
        if username in users and users[username] == password:
            # # if validar_codigo(code):
            insert_user_in_logs(username, 0)
            return {'message': 'Login successful!'}, 200
            # else:
            #     return jsonify({'message': 'Invalid code!'}), 401
        else:
            return {'message': 'Invalid username or password!'}, 401

app = Flask(__name__)
api = Api(app)

api.add_resource(Userlogin, '/login')

if __name__ == '__main__':
    app.run(debug=True)