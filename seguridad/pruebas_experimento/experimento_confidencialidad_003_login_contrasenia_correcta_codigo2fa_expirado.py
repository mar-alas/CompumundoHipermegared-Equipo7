import requests
import random
import json
import datetime
from pruebas_experimento.experimento_utils import borrar_archivos_previo_experimento
import string
import random
import pyotp
import time

URL = "http://127.0.0.1:5000"
ENDPOINT = "/login"
NUM_REQUESTS = 500
NOMBRE_EXPERIMENTO = "experimento_confidencialidad_002_login_contrasenia_correcta_codigo2fa_expirado"
CATEGORIA = "confidencialidad"
TIPO_RESULTADO = "status_code"
LOGIN_LIMITER_MAX = "1"

borrar_archivos_previo_experimento()

def correr_prueba():
    print(f"Generar {NUM_REQUESTS} intentos de log in con un usuario correcto y "
          f"contrasenas correctas, codigo correcto pero expirado")
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    request_enviados=[]
    request_enviados.append("fecha;nombre_experimento;categoria;id_request;request;response;tipo_resultado;resultado_esperado;resultado_obtenido;LOGIN_LIMITER_MAX")
    
    for intento in range(0, NUM_REQUESTS):
        correo = random.choice(["dgamez@gmail.com", "jhon@gmail.com", "maria@gmail.com", "robert@gmail.com"])
        password = "Password1!"
        fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        codigo_generado = pyotp.parse_uri(f'otpauth://totp/ExperimentoSeguridad:{correo}?secret=UniandesArquitectura&issuer=ExperimentoSeguridad')
        codigo = codigo_generado.now()
        json_data = {
            'username': correo,
            'password': password,
            'code': codigo
        }
        time.sleep(30)
        response = requests.post(f'{URL}{ENDPOINT}', headers=headers, json=json_data)
        content =  json.loads(response.content.decode())
        request_enviados.append(";".join([fecha, NOMBRE_EXPERIMENTO, CATEGORIA, str(intento),
                                          str(json_data).strip('\n'), str(content).strip('\n'),
                                          TIPO_RESULTADO, "401", str(response.status_code), LOGIN_LIMITER_MAX]))
    return request_enviados


def guardar_logs(lista, archivo):
    with open(archivo, mode='w+', encoding='utf-8') as logs:
            logs.write('\n'.join(lista))
            logs.write('\n')

request_enviados = correr_prueba()
guardar_logs(request_enviados, "pruebas_experimento/resultados_experimentos/resultado_experimento_confidencialidad_0002.csv")