from flask import Flask
from flask_restful import Api, Resource, reqparse

app = Flask(__name__)
api = Api(app)


class UserResource(Resource):

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('email', type=str, required=True, help='Email address is required')
        args = parser.parse_args()
        email = args['email']

        return {'message': 'Email received successfully', 'status':'success'}, 200
    
api.add_resource(UserResource, '/api/v1/users')

if __name__ == '__main__':
    app.run(debug=True)