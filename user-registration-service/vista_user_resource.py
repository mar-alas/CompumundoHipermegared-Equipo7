from flask_restful import Resource, reqparse
from queues.queue_failures_with_user_registration_log import registrar_falla_en_registro
from queues.queue_user_registration_service_principal import registrar_usuario_principal
from queues.queue_user_registration_service_redundancia1 import registrar_usuario_redundancia1
from queues.queue_user_registration_service_redundancia2 import registrar_usuario_redundancia2
import datetime


class UserResource(Resource):

    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('email', type=str, required=True, help='Email address is required')
            parser.add_argument('simulate_failure', type=bool, required=False)
            parser.add_argument('simulate_failure_r1', type=bool, required=False)
            parser.add_argument('failure_uuid', type=str, required=False)
            args = parser.parse_args()
            email = args['email']

            if 'simulate_failure' in args and args['simulate_failure'] is True:
                failure_uuid = args['failure_uuid']
                failure_datetime = str(datetime.datetime.now())

                if 'simulate_failure_r1' in args and args['simulate_failure_r1'] is True:
                    registrar_usuario_redundancia2.delay(email)
                else:
                    registrar_usuario_redundancia1.delay(email)

                raise Exception(str(failure_uuid) + ";" + email + ";" + str(failure_datetime))

            registrar_usuario_principal.delay(email)

        except Exception as e:
            error_message = str(e)
            registrar_falla_en_registro.delay(error_message)
            return {
                'status': 'success',
                'message': ('Email received successfully. We are experiencing latencies '
                            'but we received your email and we will register you.')
            }, 200

        return {'status': 'success', 'message': 'Email received successfully'}, 200
