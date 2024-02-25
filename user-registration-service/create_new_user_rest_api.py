from flask import Flask
from flask_restful import Api
from vista_user_resource import UserResource
from vista_ping_resource import PingResource

app = Flask(__name__)
api = Api(app)

api.add_resource(UserResource, '/api/v1/users')
api.add_resource(PingResource, '/ping')

if __name__ == '__main__':
    app.run(debug=True)