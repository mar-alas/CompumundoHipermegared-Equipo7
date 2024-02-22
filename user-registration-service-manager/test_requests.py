import requests
import random
import string
import uuid

url = "http://127.0.0.1:3000"
endpoint = "/api/v1/users"
numero_requests = 10
porcentaje_fallo = 0.1

def generar_correo(numero_caracteres=10):
    dominios = [ "hotmail.com", "gmail.com", "aol.com", "mail.com" , "mail.kz", "yahoo.com"]
    letras = string.ascii_lowercase[:12]
    dominio = random.choice(dominios)
    nombre = ''.join(random.choice(letras) for i in range(numero_caracteres))
    return f'{nombre}@{dominio}'

headers = {
    'Content-Type': 'application/json',
}

fallos = int(numero_requests*porcentaje_fallo)
print(f"Numero de request a generar {numero_requests} con un porcentaje de fallo de {porcentaje_fallo} equivalente a {fallos} fallos")
bool_list = [False] * fallos + [True] * (numero_requests - fallos)
random.shuffle(bool_list)
for resultado in bool_list:
    # si resultado es positivo que haga un request que funcione bien
    if resultado:
        json_data = {
            'email': generar_correo(),
        }
        response = requests.post(f'{url}{endpoint}', headers=headers, json=json_data)
        assert response.ok, "Fallo el request"
    else:
        # que haga un request con fallo
        json_data = {
            'email': generar_correo(),
            'simulate_failure': True,
            "failure_uuid": str(uuid.uuid4())
        }
        response = requests.post(f'{url}{endpoint}', headers=headers, json=json_data)
        assert response.ok, "Fallo el request"
