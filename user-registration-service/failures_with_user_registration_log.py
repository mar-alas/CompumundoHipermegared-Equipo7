#celery -A failures_with_user_registration_log worker --loglevel=info
from celery import Celery
import os

celery = Celery('user_registration_failures_logs', broker='redis://localhost:6379/2')

def insert_failure_in_db(failure_data):
    #check if the file exists
    if not os.path.exists("user_registration_failures_logs.csv"):
        # Create the file with the header
        with open("user_registration_failures_logs.csv", mode='w', encoding='utf-8') as file:
            file.write("id;correo;fecha\n")

    file_name = "user_registration_failures_logs.csv"
    with open(file_name, mode='a', encoding='utf-8') as file:
        file.write(failure_data+"\n")


@celery.task
def registrar_falla_en_registro(failure_data):
    insert_failure_in_db(failure_data)