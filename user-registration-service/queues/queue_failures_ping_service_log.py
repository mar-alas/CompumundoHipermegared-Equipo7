#celery -A failures_ping_service_log worker --loglevel=info

from celery import Celery
import os

celery = Celery('ping_logs', broker='redis://localhost:6379/6')


def insert_ping_in_db_fallos(error):

    file_name = "database/ping_logs_error.csv"

    # Check if the file exists
    if not os.path.exists(file_name):
        # Create the file with the header
        with open(file_name, mode='w', encoding='utf-8') as file:
            file.write("id;fecha\n")


    with open(file_name, mode='a', encoding='utf-8') as file:
        file.write(f"{error}\n")


@celery.task(name="queues.queue_failures_ping_service_log.registrar_ping_falla")
def registrar_ping_falla(error):
    insert_ping_in_db_fallos(error)
