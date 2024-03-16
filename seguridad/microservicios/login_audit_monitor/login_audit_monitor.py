#autor: Daniel Gamez
#este codigo revisa si en los lgos login_logs.csv hay usuarios con mas de 3 logins no exitosos
# e imprime el resultado en el archivo logs_login_audit_monitor.txt
#este codigo se debe correr desde la base del proyecto con el comando:
#python3 seguridad/microservicios/login_audit_monitor/login_audit_monitor.py

import pandas as pd
import time
import os

umbral_login_no_exitoso = 3

ruta_logs_auditor_csv="seguridad/microservicios/base_datos/table_logs_login_audit_monitor.csv"

#if os.path.exists(ruta_logs_auditor_csv):
#            os.remove(ruta_logs_auditor_csv)

ruta_login_logs="seguridad/microservicios/base_datos/table_login_logs.csv"


def revision_logins_no_exitosos():
    login_logs = pd.read_csv(ruta_login_logs, sep=';')
    logins_no_exitosos = login_logs[login_logs['login_exitoso'] == 0]
    logins_no_exitosos_por_usuario = logins_no_exitosos['usuario'].value_counts()
    logins_no_exitosos_por_usuario_sospechosos = logins_no_exitosos_por_usuario[logins_no_exitosos_por_usuario > umbral_login_no_exitoso]

    existe_csv=os.path.exists(ruta_logs_auditor_csv)
    logs_auditor=pd.DataFrame({"usuario":[]})	
    if existe_csv:
        logs_auditor=pd.read_csv(ruta_logs_auditor_csv, sep=';')

    fecha=time.strftime("%Y-%m-%d %H:%M:%S")

    if not logins_no_exitosos_por_usuario_sospechosos.empty:
        for user_ataque in logins_no_exitosos_por_usuario_sospechosos.index:
            #solo se imprime el ataque si no ha sido reportado antes
            if logs_auditor[logs_auditor['usuario']==user_ataque].empty:
                mensaje= " ALERTA Usuario "+ user_ataque +" con mas de "+ str(umbral_login_no_exitoso) +" logins no exitosos"
                print(fecha + mensaje)
                existe_csv=os.path.exists(ruta_logs_auditor_csv)
                df_log = pd.DataFrame({'Fecha': [fecha],'Tipo_Alerta':'MULTIPLE_LOGINS', 'Mensaje': [mensaje],'usuario': [user_ataque]})
                df_log.to_csv(ruta_logs_auditor_csv, mode='a', header=not(existe_csv), index=False, sep=';')

    else:
        mensaje=fecha + "No hay usuarios con mas de 3 logins no exitosos"
        print(mensaje)
        

try:
    while True:
        revision_logins_no_exitosos()
        time.sleep(2)

except KeyboardInterrupt:
    print("\nKeyboard interrupt received. Exiting...")



