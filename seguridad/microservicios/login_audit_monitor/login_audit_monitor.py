#este codigo revisa si en los lgos login_logs.csv hay usuarios con mas de 3 logins no exitosos
# e imprime el resultado en el archivo logs_login_audit_monitor.txt
import pandas as pd
import time
import os

umbral_login_no_exitoso = 3


ruta_logs_auditor="seguridad/microservicios/login_audit_monitor/logs_login_audit_monitor.txt"

if os.path.exists(ruta_logs_auditor):
            os.remove(ruta_logs_auditor)

ruta_csv="seguridad/microservicios/login_audit_monitor/login_logs.csv"
login_logs = pd.read_csv(ruta_csv, sep=';')

def revision_logins_no_exitosos():

    logins_no_exitosos = login_logs[login_logs['Exitoso'] == 0]
    logins_no_exitosos_por_usuario = logins_no_exitosos['Usuario'].value_counts()
    logins_no_exitosos_por_usuario_sospechosos = logins_no_exitosos_por_usuario[logins_no_exitosos_por_usuario > umbral_login_no_exitoso]

    fecha=time.strftime("%Y-%m-%d %H:%M:%S")

    if not logins_no_exitosos_por_usuario_sospechosos.empty:
        mensaje=fecha + " ALERTA Usuarios con más de "+ str(umbral_login_no_exitoso) +" logins no exitosos"
        print(mensaje)
        with open(ruta_logs_auditor, 'a') as f:
            f.write(mensaje + "\n")
    else:
        mensaje=fecha + "No hay usuarios con más de 3 logins no exitosos"
        print(mensaje)
        with open(ruta_logs_auditor, 'a') as f:
            f.write(mensaje+"\n")

contador = 0
while contador<3:
    revision_logins_no_exitosos()
    contador += 1
    time.sleep(2)





