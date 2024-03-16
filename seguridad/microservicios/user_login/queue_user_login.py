#se corre desde la carpeta de user_login
#this celery runs with the command: celery -A queue_user_login worker --loglevel=info
from celery import Celery
import os
from datetime import datetime

celery = Celery('tasks', broker='redis://localhost:6379/0')

def insert_user_in_logs(username, exitoso):
    file_name = "seguridad/microservicios/base_datos/table_login_logs.csv"
    print(f"LOCATION: {os.getcwd()}")
    # Check if the file exists
    if not os.path.exists(file_name):
        # Create the file with the header
        with open(file_name, mode='w', encoding='utf-8') as file:
            file.write("Fecha;Usuario;Contrasenia;Exitoso\n")

    # Open the file in write mode ("w")
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    with open(file_name, mode='a', encoding='utf-8') as file:
        file.write(f"{fecha};{username};{exitoso}\n")


@celery.task(name="queues.queue_user_login.login_usuario")
def login_usuario(username, exitoso):
    insert_user_in_logs(username, exitoso)
