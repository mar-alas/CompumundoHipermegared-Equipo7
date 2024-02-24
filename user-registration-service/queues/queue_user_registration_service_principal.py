from celery import Celery

celery = Celery('tasks', broker='redis://localhost:6379/0')


def insert_user_in_db(email):
    file_name = "database/usuarios_db.csv"

    # Open the file in write mode ("w")
    with open(file_name, mode='a', encoding='utf-8') as file:
        file.write(email + ";principal" + "\n")


@celery.task(name="queues.queue_user_registration_service_redundancia2.registrar_usuario_principal")
def registrar_usuario_principal(email):
    insert_user_in_db(email)
