import requests
import random
import string
import uuid
from faker import Faker
import json
import os
import datetime
import time
import json

URL = "http://127.0.0.1:3000"
ENDPOINT = "/api/v1/users"
ENDPOINT_PING = "/ping"
NUM_REQUESTS = 100
PORCENTAJE_FALLO = 0.1

#set a seed for reproducibility
random.seed(0)
Faker.seed(0)

#se borran los archivos del experimento previo en caso de que exista
file_path_ping_enviados = "pruebas_experimento/ping_enviados.csv"
file_path_request_usuarios_enviados = "pruebas_experimento/request_usuarios_enviados.csv"
file_path_request_usuarios_enviados_r2 = "pruebas_experimento/request_usuarios_enviados_r2.csv"

file_path_ping_logs = "user-registration-service/queues/database/ping_logs.csv"
file_path_user_registration_logs = "user-registration-service/queues/database/user_registration_logs.csv"
file_path_usuarios_db = "user-registration-service/queues/database/usuarios_db.csv"
file_path_user_registration_failures_logs = "user-registration-service/queues/database/user_registration_failures_logs.csv"
file_path_ping_logs_error = "user-registration-service/queues/database/ping_logs_error.csv"

if os.path.exists(file_path_ping_enviados):
    os.remove(file_path_ping_enviados)
    print(f"Archivo {file_path_ping_enviados} borrado con exito")

if os.path.exists(file_path_request_usuarios_enviados):
    os.remove(file_path_request_usuarios_enviados)
    print(f"Archivo {file_path_request_usuarios_enviados} borrado con exito")

if os.path.exists(file_path_request_usuarios_enviados_r2):
    os.remove(file_path_request_usuarios_enviados_r2)
    print(f"Archivo {file_path_request_usuarios_enviados_r2} borrado con exito")

if os.path.exists(file_path_ping_logs):
    os.remove(file_path_ping_logs)
    print(f"Archivo {file_path_ping_logs} borrado con exito")

if os.path.exists(file_path_user_registration_logs):
    os.remove(file_path_user_registration_logs)
    print(f"Archivo {file_path_user_registration_logs} borrado con exito")

if os.path.exists(file_path_usuarios_db):
    os.remove(file_path_usuarios_db)
    print(f"Archivo {file_path_usuarios_db} borrado con exito")

if os.path.exists(file_path_user_registration_failures_logs):
    os.remove(file_path_user_registration_failures_logs)
    print(f"Archivo {file_path_user_registration_failures_logs} borrado con exito")

if os.path.exists(file_path_ping_logs_error):
    os.remove(file_path_ping_logs_error)
    print(f"Archivo {file_path_ping_logs_error} borrado con exito")


def correr_prueba_registro(simulate_failure):
    fallos = int(NUM_REQUESTS * PORCENTAJE_FALLO)
    print(f"Numero de request a generar {NUM_REQUESTS} para registrar usuarios "
          f"con un porcentaje de fallo de {PORCENTAJE_FALLO} equivalente a {fallos} fallos")
    bool_list = [False] * fallos + [True] * (NUM_REQUESTS - fallos)
    random.shuffle(bool_list)

    headers = {
        'Content-Type': 'application/json',
    }
    request_enviados=[]
    request_enviados.append("fecha;email;resultado;fecha_respuesta;respuesta_servidor")
    
    fake = Faker()
    for resultado in bool_list:
        #wait half a second
        #time.sleep(0.5)

        # si resultado es positivo que haga un request que funcione bien
        correo = fake.email()
        fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        if resultado:
            json_data = {
                'email': correo,
            }
            response = requests.post(f'{URL}{ENDPOINT}', headers=headers, json=json_data)

            # Assuming 'response' is the JSON response
            response_json = response.json()
            message = response_json['message']
            message_str = json.dumps(message)


            fecha_respuesta = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
            assert response.ok, "Fallo el request"
            request_enviados.append(";".join([fecha, correo, "POSITIVO", fecha_respuesta, message_str]))

        else:
            # que haga un request con fallo
            json_data = {
                'email': correo,
                'simulate_failure': simulate_failure["simulate_failure"],
                'simulate_failure_r1': simulate_failure["simulate_failure_r1"],
                # 'simulate_failure_r2': simulate_failure["simulate_failure_r2"],
                "failure_uuid": str(uuid.uuid4())
            }
            response = requests.post(f'{URL}{ENDPOINT}', headers=headers, json=json_data)

            # Assuming 'response' is the JSON response
            response_json = response.json()
            message = response_json['message']
            message_str = json.dumps(message)


            fecha_respuesta = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")

            assert response.ok, "Fallo el request"
            message_str = json.dumps(message)
            request_enviados.append(";".join([fecha, correo, "NEGATIVO", fecha_respuesta, message_str]))

    return request_enviados


def guardar_logs(lista, archivo):
    with open(archivo, mode='w+', encoding='utf-8') as logs:
            logs.write('\n'.join(lista))
            logs.write('\n')


def correr_prueba_ping():
    fallos = int(NUM_REQUESTS * PORCENTAJE_FALLO)
    print(f"Numero de PING requests a generar {NUM_REQUESTS} con un porcentaje "
          f"de fallo de {PORCENTAJE_FALLO} equivalente a {fallos} fallos")
    bool_list = [False] * fallos + [True] * (NUM_REQUESTS - fallos)
    random.shuffle(bool_list)

    headers = {
        'Content-Type': 'application/json',
    }
    pings_enviados = []
    pings_enviados.append("ping_id;ping_datetime;resultado")

    for resultado in bool_list:
        # si resultado es positivo que haga un request que funcione bien
        if resultado:
            response = requests.get(f'{URL}{ENDPOINT_PING}', headers=headers)
            assert response.ok, "Fallo el request"
            data = json.loads(response.text)
            pings_enviados.append(f"{data['ping_id']};{data['ping_datetime']};POSITIVO")
        else:
            # que haga un request con fallo
            response = requests.get(f'{URL}{ENDPOINT_PING}?simulate_failure', headers=headers)
            assert response.ok, "Fallo el request"
            data = json.loads(response.text)
            pings_enviados.append(f"{data['ping_id']};{data['ping_datetime']};NEGATIVO")
    return pings_enviados

simulate_failure = {"simulate_failure": True, "simulate_failure_r1": False, "simulate_failure_r3": False}
request_enviados = correr_prueba_registro(simulate_failure)
guardar_logs(request_enviados, file_path_request_usuarios_enviados)

simulate_failure = {"simulate_failure": False, "simulate_failure_r1": True, "simulate_failure_r3": False}
request_enviados = correr_prueba_registro(simulate_failure)
guardar_logs(request_enviados, file_path_request_usuarios_enviados_r2)

pings_enviados = correr_prueba_ping()
guardar_logs(pings_enviados, file_path_ping_enviados)