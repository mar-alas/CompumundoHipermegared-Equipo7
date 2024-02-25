from celery import Celery

# Create a Celery instance
celery = Celery('tasks', broker='redis://localhost:6379/4')


def insert_user_in_db(email):
    file_name = "database/usuarios_db.csv"
    with open(file_name, mode='a', encoding='utf-8') as file:
        file.write(email + ";redundancia2" + "\n")


# Define a Celery task
@celery.task(name="queues.queue_user_registration_service_redundancia2.registrar_usuario_redundancia2")
def registrar_usuario_redundancia2(email):
    insert_user_in_db(email)
