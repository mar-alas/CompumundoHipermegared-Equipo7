import pandas as pd

def validar_datos_usuario(username, password):
    ruta_tabla_usuarios="seguridad/microservicios/base_datos/table_usuarios.csv"
    tabla_usuarios=pd.read_csv(ruta_tabla_usuarios,sep=";",header=0)
    user_logeado=tabla_usuarios[(tabla_usuarios["usuario"]==username) & (tabla_usuarios["contrasenia"]==password)]
    if not user_logeado.empty:
        return True
    else:
        return False
