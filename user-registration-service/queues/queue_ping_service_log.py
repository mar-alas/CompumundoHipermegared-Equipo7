#celery -A ping_service_log worker --loglevel=info
from celery import Celery
import os

celery = Celery('ping_logs', broker='redis://localhost:6379/1')


def insert_ping_in_db(ping_id, date):
    file_name = "database/ping_logs.csv"
    # Check if the file exists
    if not os.path.exists(file_name):
        # Create the file with the header
        with open(file_name, mode='w', encoding='utf-8') as file:
            file.write("ping_id,date\n")
            
    with open(file_name, mode='a', encoding='utf-8') as file:
        file.write(ping_id+","+date+"\n")




@celery.task(name="queues.ping_service_log.registrar_ping_recibido")
def registrar_ping_recibido(ping_id, ping_datetime):
    insert_ping_in_db(ping_id, ping_datetime)
