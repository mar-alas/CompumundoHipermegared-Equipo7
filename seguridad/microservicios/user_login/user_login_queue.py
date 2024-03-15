#this celery runs with the command: celery -A user_login_queue.celery worker --loglevel=info
from celery import Celery
import os

celery = Celery('tasks', broker='redis://localhost:6379/0')


def insert_user_in_db(email):
    file_name = "database/usuarios_db.csv"
    # Check if the file exists
    if not os.path.exists(file_name):
        # Create the file with the header
        with open(file_name, mode='w', encoding='utf-8') as file:
            file.write("email;componente_registrador\n")

    # Open the file in write mode ("w")
    with open(file_name, mode='a', encoding='utf-8') as file:
        file.write(email + ";principal" + "\n")


@celery.task(name="queues.queue_user_registration_service_principal.registrar_usuario_principal")
def registrar_usuario_principal(email):
    insert_user_in_db(email)
