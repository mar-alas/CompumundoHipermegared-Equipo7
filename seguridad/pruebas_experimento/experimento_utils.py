#este archivo tiene funciones de soporte para el archivo test_requests.py

import os

def borrar_archivos_previo_experimento():
    file_paths = [
        "pruebas_experimento/ping_enviados.csv",
        "pruebas_experimento/request_usuarios_enviados_fallacompprinc.csv",
        "pruebas_experimento/request_usuarios_enviados_fallaredund1.csv",
        "user-registration-service/queues/database/ping_logs.csv",
        "user-registration-service/queues/database/user_registration_logs.csv",
        "user-registration-service/queues/database/usuarios_db.csv",
        "user-registration-service/queues/database/user_registration_failures_logs.csv",
        "user-registration-service/queues/database/ping_logs_error.csv"
    ]

    for file_path in file_paths:
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"Archivo {file_path} borrado con exito")
