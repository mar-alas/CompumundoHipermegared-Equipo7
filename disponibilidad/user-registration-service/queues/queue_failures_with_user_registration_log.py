#celery -A failures_with_user_registration_log worker --loglevel=info
from celery import Celery
import os

celery = Celery('user_registration_failures_logs', broker='redis://localhost:6379/2')


def insert_failure_in_db(failure_data):

    file_name = "database/user_registration_failures_logs.csv"

    #check if the file exists
    if not os.path.exists(file_name):
        # Create the file with the header
        with open(file_name, mode='w', encoding='utf-8') as file:
            file.write("id;correo;fecha\n")


    with open(file_name, mode='a', encoding='utf-8') as file:
        file.write(failure_data + "\n")


@celery.task(name="queues.queue_failures_with_user_registration_log.registrar_falla_en_registro")
def registrar_falla_en_registro(failure_data):
    insert_failure_in_db(failure_data)
