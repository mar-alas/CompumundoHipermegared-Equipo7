import requests
import random
import string
import uuid
from faker import Faker
import json

URL = "http://127.0.0.1:3000"
ENDPOINT = "/api/v1/users"
ENDPOINT_PING = "/ping"
NUM_REQUESTS = 10
PORCENTAJE_FALLO = 0.1


def correr_prueba_registro():
    fallos = int(NUM_REQUESTS * PORCENTAJE_FALLO)
    print(f"Numero de request a generar {NUM_REQUESTS} para registrar usuarios "
          "con un porcentaje de fallo de {PORCENTAJE_FALLO} equivalente a {fallos} fallos")
    bool_list = [False] * fallos + [True] * (NUM_REQUESTS - fallos)
    random.shuffle(bool_list)

    headers = {
        'Content-Type': 'application/json',
    }
    positivo = []
    negativo = []
    fake = Faker()
    for resultado in bool_list:
        # si resultado es positivo que haga un request que funcione bien
        correo = fake.email()
        if resultado:
            json_data = {
                'email': correo,
            }
            response = requests.post(f'{URL}{ENDPOINT}', headers=headers, json=json_data)
            assert response.ok, "Fallo el request"
            positivo.append(correo)
        else:
            # que haga un request con fallo
            json_data = {
                'email': correo,
                'simulate_failure': True,
                "failure_uuid": str(uuid.uuid4())
            }
            response = requests.post(f'{URL}{ENDPOINT}', headers=headers, json=json_data)
            assert response.ok, "Fallo el request"
            negativo.append(correo)
    return positivo, negativo


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
    positivo = []
    negativo = []
    for resultado in bool_list:
        # si resultado es positivo que haga un request que funcione bien
        if resultado:
            response = requests.get(f'{URL}{ENDPOINT_PING}', headers=headers)
            assert response.ok, "Fallo el request"
            data = json.loads(response.text)
            positivo.append(f"{data['ping_id']};{data['ping_datetime']}")
        else:
            # que haga un request con fallo
            response = requests.get(f'{URL}{ENDPOINT_PING}?simulate_failure', headers=headers)
            assert response.ok, "Fallo el request"
            data = json.loads(response.text)
            negativo.append(f"{data['ping_id']};{data['ping_datetime']}")
    return positivo, negativo

positivo, negativo = correr_prueba_registro()
guardar_logs(positivo, "pruebas_experimento/request_usuarios_enviados_no_err.csv")
guardar_logs(negativo, "pruebas_experimento/request_usuarios_enviados_err.csv")
positivo, negativo = correr_prueba_ping()
guardar_logs(positivo, "pruebas_experimento/ping_enviados_no_err.csv")
guardar_logs(negativo, "pruebas_experimento/ping_enviados_err.csv")