#este codigo revisa si en los lgos login_logs.csv hay usuarios con mas de 3 logins no exitosos
# e imprime el resultado
import pandas as pd
import time

umbral_login_no_exitoso = 3

ruta_csv="seguridad/microservicios/login_audit_monitor/login_logs.csv"
login_logs = pd.read_csv(ruta_csv, sep=';')

def revision_logins_no_exitosos():

    logins_no_exitosos = login_logs[login_logs['Exitoso'] == 0]
    logins_no_exitosos_por_usuario = logins_no_exitosos['Usuario'].value_counts()
    logins_no_exitosos_por_usuario_sospechosos = logins_no_exitosos_por_usuario[logins_no_exitosos_por_usuario > umbral_login_no_exitoso]

    fecha=time.strftime("%Y-%m-%d %H:%M:%S")

    if not logins_no_exitosos_por_usuario_sospechosos.empty:
        mensaje=fecha + " ALTERTA Usuarios con más de "+ str(umbral_login_no_exitoso) +" logins no exitosos"
        print(mensaje)
        with open('seguridad/microservicios/login_audit_monitor/alertas.txt', 'a') as f:
            f.write(mensaje + "\n")
    else:
        mensaje=fecha + "No hay usuarios con más de 3 logins no exitosos"
        print(mensaje)
        with open('seguridad/microservicios/login_audit_monitor/alertas.txt', 'a') as f:
            f.write(mensaje+"\n")

contador = 0
while contador<10:
    revision_logins_no_exitosos()
    contador += 1
    time.sleep(2)





