#este codigo revisa si en los lgos login_logs.csv hay usuarios con mas de 3 logins no exitosos
# e imprime el resultado en el archivo logs_login_audit_monitor.txt
import pandas as pd
import time
import os

umbral_login_no_exitoso = 3


ruta_logs_auditor="seguridad/microservicios/login_audit_monitor/logs_login_audit_monitor.txt"
ruta_logs_auditor_csv="seguridad/microservicios/base_datos/table_logs_login_audit_monitor.csv"

if os.path.exists(ruta_logs_auditor):
            os.remove(ruta_logs_auditor)

#if os.path.exists(ruta_logs_auditor_csv):
#            os.remove(ruta_logs_auditor_csv)

ruta_login_logs="seguridad/microservicios/base_datos/table_login_logs.csv"
login_logs = pd.read_csv(ruta_login_logs, sep=';')

def revision_logins_no_exitosos():

    logins_no_exitosos = login_logs[login_logs['login_exitoso'] == 0]
    logins_no_exitosos_por_usuario = logins_no_exitosos['usuario'].value_counts()
    logins_no_exitosos_por_usuario_sospechosos = logins_no_exitosos_por_usuario[logins_no_exitosos_por_usuario > umbral_login_no_exitoso]

    fecha=time.strftime("%Y-%m-%d %H:%M:%S")

    if not logins_no_exitosos_por_usuario_sospechosos.empty:
        mensaje= " ALERTA Usuarios con mas de "+ str(umbral_login_no_exitoso) +" logins no exitosos"
        print(fecha + mensaje)
        with open(ruta_logs_auditor, 'a') as f:
            f.write(mensaje + "\n")

        existe_csv=os.path.exists(ruta_logs_auditor_csv)
        df_log = pd.DataFrame({'Fecha': [fecha],'Tipo_Alerta':'MULTIPLE_LOGINS', 'Mensaje': [mensaje]})
        df_log.to_csv(ruta_logs_auditor_csv, mode='a', header=not(existe_csv), index=False, sep=';')

    else:
        mensaje=fecha + "No hay usuarios con mas de 3 logins no exitosos"
        print(mensaje)
        with open(ruta_logs_auditor, 'a') as f:
            f.write(mensaje+"\n")

contador = 0
while contador<3:
    revision_logins_no_exitosos()
    contador += 1
    time.sleep(2)





