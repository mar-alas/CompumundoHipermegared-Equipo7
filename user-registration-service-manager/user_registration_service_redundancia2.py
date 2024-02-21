from celery import Celery

# Create a Celery instance
celery = Celery('tasks', broker='redis://localhost:6379/0')

def insert_user_in_db(email):
    file_name = "data.txt"
    
    # Open the file in write mode ("w")
    with open(file_name, "a") as file:
        # Write content into the file
        file.write(email+",redundancia2"+"\n")
        #raise Exception("Falla a proposito. "+email)

# Define a Celery task
@celery.task
def registrar_usuario_redundancia2(email):
    insert_user_in_db(email)