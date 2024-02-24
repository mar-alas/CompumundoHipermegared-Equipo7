from ping_service_log import registrar_ping_recibido
from failures_ping_service_log import registrar_ping_falla
from flask_restful import  Resource

import uuid
import datetime

class PingResource(Resource):
    def get(self):
        new_ping_id = str(uuid.uuid4())
        new_ping_datetime = str(datetime.datetime.now())
        try:
            if 'simulate_failure' in  request.args:
                raise Exception(str(new_ping_id) + ";" + str(new_ping_datetime))
            else:
                registrar_ping_recibido.delay(ping_id=new_ping_id,
                                              ping_datetime=new_ping_datetime)
                return {
                    'status': 'success',
                    'message': 'Echo',
                    "ping_id":new_ping_id,
                    "ping_datetime":new_ping_datetime
                }, 200
        except Exception as e:
            error_message = str(e)
            registrar_ping_falla.delay(error_message)
            return {
                'status':'success',
                "ping_id":new_ping_id,
                "ping_datetime":new_ping_datetime,
                'message': 'Ping failure received.'
            }, 200