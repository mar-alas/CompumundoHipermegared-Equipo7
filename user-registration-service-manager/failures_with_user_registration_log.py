from celery import Celery

celery = Celery('user_registration_failures_logs', broker='redis://localhost:6379/0')

def insert_failure_in_db(failure_data):
    file_name = "user_registration_failures_logs.txt"
    with open(file_name, "a") as file:
        file.write(failure_data+"\n")


@celery.task
def registrar_falla_en_registro(failure_data):
    insert_failure_in_db(failure_data)