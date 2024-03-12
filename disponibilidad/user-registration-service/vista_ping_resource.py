from flask_restful import Resource
from flask import request
import uuid
import datetime

from queues.queue_ping_service_log import registrar_ping_recibido
from queues.queue_failures_ping_service_log import registrar_ping_falla

class PingResource(Resource):
    def get(self):
        new_ping_id = str(uuid.uuid4())
        new_ping_datetime = str(datetime.datetime.now())
        try:
            simulate_failure = request.args.get('simulate_failure', type=bool, default=False)
            simulate_failure_r1 = request.args.get('simulate_failure_r1', type=bool, default=False)
            simulate_failure_r2 = request.args.get('simulate_failure_r2', type=bool, default=False)

            if simulate_failure:
                if simulate_failure_r1:
                    if simulate_failure_r2:
                        # Todos los intentos de ping fallaron
                        raise Exception(str(new_ping_id) + ";" + str(new_ping_datetime))
                    else:
                        # Falla el ping principal y redundancia1
                        registrar_ping_falla.delay(new_ping_id, new_ping_datetime)
                else:
                    # Falla solo el ping principal
                    registrar_ping_falla.delay(new_ping_id, new_ping_datetime)
            else:
                # Sin fallos, registra el ping exitosamente
                registrar_ping_recibido.delay(ping_id=new_ping_id, ping_datetime=new_ping_datetime)
                return {
                    'status': 'success',
                    'message': 'Echo',
                    "ping_id": new_ping_id,
                    "ping_datetime": new_ping_datetime
                }, 200

        except Exception as e:
            error_message = str(e)
            registrar_ping_falla.delay(error_message)
            return {
                'status': 'success',
                "ping_id": new_ping_id,
                "ping_datetime": new_ping_datetime,
                'message': 'Ping failure received.'
            }, 200
