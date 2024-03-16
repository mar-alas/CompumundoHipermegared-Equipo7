import requests
import random
import json
import datetime
from pruebas_experimento.experimento_utils import borrar_archivos_previo_experimento
import string
import random
from faker import Faker
import uuid

URL = "http://127.0.0.1:5000"
ENDPOINT = "/api/v1/users"
NUM_REQUESTS = 1000
PORCENTAJE_REQUESTS_POSITIVOS = 0.2
NOMBRE_EXPERIMENTO = "experimento_integridad_002_edicion_usuario"
CATEGORIA = "integridad"
TIPO_RESULTADO = "status_code"
LOGIN_LIMITER_MAX = "1"

borrar_archivos_previo_experimento()

def correr_prueba():
    positivos = int(NUM_REQUESTS * PORCENTAJE_REQUESTS_POSITIVOS)
    print(f"Generar {NUM_REQUESTS} intentos de editar usuarios con "
          f"{PORCENTAJE_REQUESTS_POSITIVOS} escenarios positivos")
    request_enviados=[]
    request_enviados.append("fecha;nombre_experimento;categoria;id_request;request;response;tipo_resultado;resultado_esperado;resultado_obtenido;LOGIN_LIMITER_MAX")
    bool_list = [False] * positivos + [True] * (NUM_REQUESTS - positivos)
    random.shuffle(bool_list)
    fake = Faker()
    for intento in range(0, NUM_REQUESTS):
        if not bool_list[intento]:
            headers = {
                'Content-Type': 'application/json',
                'X-certificate-data': '5d1c17c6-7d13-4d1e-8a36-5109a3e2c0d3',
                'X-certificate-keypass': '1c476dcb-5911-4d03-b8a4-f293722fdcb2',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
            }
            codigo_esperado = "200"
        else:
            headers = {
                'Content-Type': 'application/json',
                'X-certificate-data': str(uuid.uuid4()),
                'X-certificate-keypass': str(uuid.uuid4()),
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
            }
            codigo_esperado = "401"

        fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        json_data = {
            'usuario': fake.email(),
            'name': fake.name(),
            'phone': fake.phone_number()
        }
        response = requests.put(f'{URL}{ENDPOINT}', headers=headers, json=json_data)
        content =  json.loads(response.content.decode())

        request_enviados.append(";".join([fecha, NOMBRE_EXPERIMENTO, CATEGORIA, str(intento),
                                            str(json_data).strip('\n'), str(content).strip('\n'),
                                            TIPO_RESULTADO, codigo_esperado, str(response.status_code), LOGIN_LIMITER_MAX]))

    return request_enviados


def guardar_logs(lista, archivo):
    with open(archivo, mode='w+', encoding='utf-8') as logs:
            logs.write('\n'.join(lista))
            logs.write('\n')

request_enviados = correr_prueba()
guardar_logs(request_enviados, "pruebas_experimento/resultados_experimentos/resultado_experimento_integridad_edicion_usuario_002.csv")
