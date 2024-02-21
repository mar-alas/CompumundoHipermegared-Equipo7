from flask import Flask
from flask_restful import Api, Resource, reqparse
from user_registration_service_principal import registrar_usuario_principal
import uuid

app = Flask(__name__)
api = Api(app)


class UserResource(Resource):

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('email', type=str, required=True, help='Email address is required')
        args = parser.parse_args()
        email = args['email']

        registrar_usuario_principal.delay(email)
        
        return {'message': 'Email received successfully', 'status':'success'}, 200
    
api.add_resource(UserResource, '/api/v1/users')

if __name__ == '__main__':
    app.run(debug=True)