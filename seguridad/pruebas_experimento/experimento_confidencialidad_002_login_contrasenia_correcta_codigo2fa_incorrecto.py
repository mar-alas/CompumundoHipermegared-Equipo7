import requests
import random
import json
import datetime
from pruebas_experimento.experimento_utils import setup_experimento
import string
import random
import pyotp

URL = "http://127.0.0.1:5000"
ENDPOINT = "/login"
NUM_REQUESTS = 1000
PORCENTAJE_REQUESTS_POSITIVOS = 0.2
NOMBRE_EXPERIMENTO = "experimento_confidencialidad_002_login_contrasenia_correcta_codigo2fa_incorrecto"
CATEGORIA = "confidencialidad"
TIPO_RESULTADO = "status_code"
LOGIN_LIMITER_MAX = "1"

setup_experimento()

def correr_prueba():
    positivos = int(NUM_REQUESTS * PORCENTAJE_REQUESTS_POSITIVOS)
    print(f"Generar {NUM_REQUESTS} intentos de log in con un usuario correcto y "
          f"contrasenas correcta, con codigo incorrecto excepto {positivos} veces")
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    }
    request_enviados=[]
    request_enviados.append("fecha;nombre_experimento;categoria;id_request;request;response;tipo_resultado;resultado_esperado;resultado_obtenido;LOGIN_LIMITER_MAX")

    bool_list = [False] * positivos + [True] * (NUM_REQUESTS - positivos)
    random.shuffle(bool_list)
    for intento in range(0, NUM_REQUESTS):
        correo = random.choice(["dgamez@gmail.com", "jhon@gmail.com", "maria@gmail.com", "robert@gmail.com"])
        if not bool_list[intento]:
            codigo_generado = pyotp.parse_uri(f'otpauth://totp/ExperimentoSeguridad:{correo}?secret=UniandesArquitectura&issuer=ExperimentoSeguridad')
            codigo = codigo_generado.now()
            codigo_esperado = "200"
        else:
            codigo = f'{random.randint(0,9)}{random.randint(0,9)}{random.randint(0,9)}{random.randint(0,9)}'
            codigo_esperado = "401"
        password = "Password1!"
        fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        json_data = {
            'username': correo,
            'password': password,
            'code': codigo
        }
        response = requests.post(f'{URL}{ENDPOINT}', headers=headers, json=json_data)
        content =  json.loads(response.content.decode())

        request_enviados.append(";".join([fecha, NOMBRE_EXPERIMENTO, CATEGORIA, str(intento),
                                          str(json_data).strip('\n'), str(content).strip('\n'),
                                          TIPO_RESULTADO, codigo_esperado, str(response.status_code),
                                          LOGIN_LIMITER_MAX]))
    return request_enviados


def guardar_logs(lista, archivo):
    with open(archivo, mode='w+', encoding='utf-8') as logs:
            logs.write('\n'.join(lista))
            logs.write('\n')

request_enviados = correr_prueba()
guardar_logs(request_enviados, "pruebas_experimento/resultados_experimentos/resultado_experimento_confidencialidad_002.csv")
