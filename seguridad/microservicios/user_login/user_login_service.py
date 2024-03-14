from flask import Flask, request, jsonify, abort
from flask_restful import Resource, reqparse
from queue_user_login import insert_user_in_logs
from flask_restful import Api

app = Flask(__name__)
api = Api(app)

# TODO: Cambiar AQUI el tamaño maximo de request que vamos a permitir para la prueba de seguridad.
# app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024 # 1MB
app.config['MAX_CONTENT_LENGTH'] = 1 * 1 * 10 # 

@app.before_request
def check_request_size():
    content_length = request.content_length
    max_content_length = app.config['MAX_CONTENT_LENGTH']
    print("Paso el tamaño de la request:", content_length)
    if content_length is not None and content_length > max_content_length:
        abort(413)  # 413 : Payload Too Large



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

api.add_resource(Userlogin, '/login')

if __name__ == '__main__':
    app.run(debug=True)