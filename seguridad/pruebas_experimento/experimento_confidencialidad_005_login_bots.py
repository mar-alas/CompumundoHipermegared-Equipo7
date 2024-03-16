import json
import requests
import csv
import datetime
import os
import random

url = 'http://localhost:5000/login'
n_requests = 1000

bot_user_agents = [
    "Googlebot/2.1 (+http://www.google.com/bot.html)",
    "Mozilla/5.0 (compatible; Bingbot/2.0; +http://www.bing.com/bingbot.htm)",
    "Mozilla/5.0 (compatible; Yahoo! Slurp; http://help.yahoo.com/help/us/ysearch/slurp)",
    "DuckDuckBot/1.0; (+http://duckduckgo.com/duckduckbot.html)",
    "Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)",
    "Mozilla/5.0 (compatible; YandexBot/3.0; +http://yandex.com/bots)"
]

csv_file_name = 'pruebas_experimento/resultados_experimentos/experimento_confidencialidad_005_login_bots.csv'

if not os.path.exists('resultados_experimentos'):
    os.makedirs('resultados_experimentos')

csv_headers = ['fecha', 'nombre_experimento', 'categoria', 'id_request', 'request', 'request_response', 'tipo_resultado', 'resultado_esperado', 'resultado_obtenido', 'LOGIN_LIMITER_MAX']

with open(csv_file_name, mode='w', newline='', encoding='utf-8-sig') as file:
    writer = csv.writer(file, delimiter=';', quoting=csv.QUOTE_ALL)
    writer.writerow(csv_headers)

    for i in range(n_requests):

        correo = random.choice(["dgamez@gmail.com", "jhon@gmail.com", "maria@gmail.com", "robert@gmail.com"])
        password = "Password1!"
        codigo = f'{random.randint(0,9)}{random.randint(0,9)}{random.randint(0,9)}{random.randint(0,9)}'
        login_data = {
            'username': correo,
            'password': password,
            'code': codigo
        }
        
        headers = {
            'User-Agent': random.choice(bot_user_agents)
        }
        response = requests.post(url, json=login_data, headers=headers)

        request_info = json.dumps(login_data) + json.dumps(headers)

        csv_data = [
            datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"),
            'experimento_confidencialidad_005_login_bots',
            'confidencialidad',
            i + 1,
            str(request_info),
            response.text,
            'status_code',
            403,
            response.status_code,
            1000
        ]

        writer.writerow(csv_data)
        print(f"Request {i + 1}: Status Code = {response.status_code}, Response = {response.text}")
