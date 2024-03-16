#este archivo tiene funciones de soporte para el archivo test_requests.py
#está diseñado para ser corrido desde la base del proyecto

import os
import pandas as pd

ruta_tabla_usuarios= "seguridad/microservicios/base_datos/table_usuarios.csv"

def borrar_archivos_previo_experimento():
    """
    Borra la data que se quiere revisar por separado en cada experimento
    """
    file_paths = [
        "seguridad/microservicios/base_datos/table_login_logs.csv",
        "seguridad/microservicios/base_datos/table_logs_edit_audit_monitor.csv",
        "seguridad/microservicios/base_datos/table_logs_login_audit_monitor.csv",
        "seguridad/microservicios/base_datos/table_usuario_edicion_logs.csv",
        ruta_tabla_usuarios
    ]

    for file_path in file_paths:
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"Archivo {file_path} borrado con exito")

def generar_base_datos():
    """
    script que genera la base de datos de usuarios para el experimento
    """
    usuarios = pd.DataFrame({
        'usuario': ['dgamez@gmail.com','jhon@gmail.com','maria@gmail.com','robert@gmail.com'],
        'contrasenia': ['Password1!','Password1!', 'Password1!', 'Password1!'],
        'nombre_usuario': ['Daniel','Jhon','Maria','Robert'],
        'fecha_insercion': ['2024-03-15 22:07:54','2024-03-15 22:07:54','2024-03-15 22:07:54','2024-03-15 22:07:54'],
        'fecha_modificacion': ['2024-03-15 22:07:54','2024-03-15 22:07:54','2024-03-15 22:07:54','2024-03-15 22:07:54']
    })
    if os.path.exists(ruta_tabla_usuarios):
        os.remove(ruta_tabla_usuarios)

    usuarios.to_csv(ruta_tabla_usuarios, index=False, header=True, sep=";")

   
def setup_experimento():
    """
    Función que prepara el sistema antes del experimento
    """
    borrar_archivos_previo_experimento()
    generar_base_datos()

def teardown_experimento():
    """
    Función que limpia el sistema después del experimento
    """
    borrar_archivos_previo_experimento()
    generar_base_datos()
    print("Experimento terminado con exito")