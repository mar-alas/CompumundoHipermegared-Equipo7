from celery import Celery

celery = Celery('ping_logs', broker='redis://localhost:6379/4')

def insert_ping_in_db_fallos(error):
    file_name = "ping_logs_error.csv"
    with open(file_name, mode='a', encoding='utf-8') as file:
        file.write(f"{error}\n")


@celery.task
def registrar_ping_falla(error):
    insert_ping_in_db_fallos(error)