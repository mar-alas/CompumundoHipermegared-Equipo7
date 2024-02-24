#celery -A ping_service_log worker --loglevel=info
from celery import Celery
import os

celery = Celery('ping_logs', broker='redis://localhost:6379/1')

def insert_ping_in_db(ping_id, date):
    # Check if the file exists
    if not os.path.exists("ping_logs.csv"):
        # Create the file with the header
        with open("ping_logs.csv", mode='w', encoding='utf-8') as file:
            file.write("ping_id,date\n")
            
    file_name = "ping_logs.csv"
    with open(file_name, mode='a', encoding='utf-8') as file:
        file.write(ping_id+","+date+"\n")

@celery.task
def registrar_ping_recibido(ping_id, ping_datetime):
    insert_ping_in_db(ping_id, ping_datetime)