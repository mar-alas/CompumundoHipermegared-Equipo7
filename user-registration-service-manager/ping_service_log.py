from celery import Celery

celery = Celery('ping_logs', broker='redis://localhost:6379/0')

def insert_ping_in_db(ping_id, date):
    file_name = "ping_logs.txt"
    with open(file_name, "a") as file:
        file.write(ping_id+","+date+"\n")


@celery.task
def registrar_ping_recibido(ping_id, ping_datetime):
    insert_ping_in_db(ping_id, ping_datetime)