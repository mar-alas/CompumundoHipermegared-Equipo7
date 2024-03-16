#este archivo tiene funciones de soporte para el archivo test_requests.py
#está diseñado para ser corrido desde la base del proyecto

import os
try:
    os.chdir("seguridad/pruebas_experimento")
except:
    pass

import pandas as pd
import time

ruta_tabla_usuarios= "../microservicios/base_datos/table_usuarios.csv"

def borrar_archivos_previo_experimento():
    """
    Borra la data que se quiere revisar por separado en cada experimento
    """
    file_paths = [
        "../microservicios/base_datos/table_login_logs.csv"
        ,"../microservicios/base_datos/table_logs_edit_audit_monitor.csv"
        ,"../microservicios/base_datos/table_logs_login_audit_monitor.csv"
        ,"../microservicios/base_datos/table_usuario_edicion_logs.csv"
        ,ruta_tabla_usuarios
    ]

    
    for file_path in file_paths:
        if os.path.exists(file_path):
            df = pd.read_csv(file_path, sep=";",header=0)
            df.drop(df.index, inplace=True)
            df.to_csv(file_path, index=False, header=True, sep=";")
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

def modificar_sin_autorizacion_bd(usuario):
    """
    Función que modifica la base de datos sin autorización
    """
    usuarios = pd.read_csv(ruta_tabla_usuarios, sep=";")
    fecha_modificacion = time.strftime("%Y-%m-%d %H:%M:%S")

    usuarios.loc[usuarios['usuario'] == usuario, 'fecha_modificacion'] = fecha_modificacion
    usuarios.to_csv(ruta_tabla_usuarios, index=False, header=True, sep=";")
    
def detectar_modificacion_sin_autorizacion_bd(usuario):
    """
    Función que detecta si la base de datos fue modificada sin autorización
    """
    ruta_logs_edit_monitor = "../microservicios/base_datos/table_logs_edit_audit_monitor.csv"
    logs_edit_monitor = pd.read_csv(ruta_logs_edit_monitor, sep=";",header=0)
    logs_edit_monitor_usuario = logs_edit_monitor[logs_edit_monitor['usuario'] == usuario]
    
    if logs_edit_monitor_usuario.empty:
        return False
    else:
        return True

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