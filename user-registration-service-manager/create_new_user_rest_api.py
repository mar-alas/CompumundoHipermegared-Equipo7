from flask import Flask
from flask_restful import Api, Resource, reqparse
from user_registration_service_principal import registrar_usuario_principal
from ping_service_log import registrar_ping_recibido

import uuid
import datetime


app = Flask(__name__)
api = Api(app)


class UserResource(Resource):

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('email', type=str, required=True, help='Email address is required')
        args = parser.parse_args()
        email = args['email']

        registrar_usuario_principal.delay(email)
        
        return {'status':'success', 'message': 'Email received successfully'}, 200
    

class PingResource(Resource):
    def get(self):
        new_ping_id = str(uuid.uuid4())
        new_ping_datetime = str(datetime.datetime.now())
        registrar_ping_recibido.delay(ping_id=new_ping_id, ping_datetime=new_ping_datetime)
        return {
            'status': 'success', 
            'message': 'Echo', 
            "ping_id":new_ping_id, 
            "ping_datetime":new_ping_datetime
        }, 200

    
api.add_resource(UserResource, '/api/v1/users')
api.add_resource(PingResource, '/ping')

if __name__ == '__main__':
    app.run(debug=True)