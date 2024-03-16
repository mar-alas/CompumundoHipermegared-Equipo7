import requests
import csv
from datetime import datetime
import os
import random

url = 'http://localhost:5000/login'
n_requests = 1000

login_data_template = {
    "username": "robert@gmail.com",
    "password": "Password1&",
    "code": "424496"
}

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

with open(csv_file_name, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file, quoting=csv.QUOTE_ALL)
    writer.writerow(csv_headers)

    for i in range(n_requests):

        login_data = login_data_template.copy()
        headers = {
            'User-Agent': random.choice(bot_user_agents)
        }
        response = requests.post(url, json=login_data, headers=headers)

        csv_data = [
            datetime.now().strftime('%d/%m/%Y'), 
            'experimento_confidencialidad_005_login_bots',
            'confidencialidad',
            i + 1,
            str(login_data),
            response.text,
            'status_code',
            403,
            response.status_code,
            1
        ]

        writer.writerow(csv_data)
        print(f"Request {i + 1}: Status Code = {response.status_code}, Response = {response.text}")
