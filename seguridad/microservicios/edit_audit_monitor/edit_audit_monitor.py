#autor: Daniel Gamez
#fecha: 15/03/2024
#este codigo revisa si hay usuarios modificados en la base de datos que no tengan logs asociados del servicio de editar
#este archivo debe correrse desde la carpeta base del proyecto con el comando:
#python3 seguridad/microservicios/edit_audit_monitor/edit_audit_monitor.py
import pandas as pd
import time
import os

ruta_logs_auditor_csv="seguridad/microservicios/base_datos/table_logs_edit_audit_monitor.csv"
ruta_edit_logs="seguridad/microservicios/base_datos/table_usuario_edicion_logs.csv"
ruta_table_usuarios = 'seguridad/microservicios/base_datos/table_usuarios.csv'

def revision_edits_no_autorizados():
    edit_logs = pd.read_csv(ruta_edit_logs, sep=';')

    df_usuarios = pd.read_csv(ruta_table_usuarios, header=0, sep=';')
    df_usuarios_modificados = df_usuarios[df_usuarios['fecha_modificacion'] != df_usuarios['fecha_insercion']]
    df_usuarios_modificados_merge = pd.merge(df_usuarios_modificados, edit_logs, on='usuario', how='left')
    df_usuarios_modificados_sin_autorizacion = df_usuarios_modificados_merge[df_usuarios_modificados_merge["fecha_log"]!=df_usuarios_modificados_merge["fecha_modificacion"]]

    existe_csv=os.path.exists(ruta_logs_auditor_csv)
    monitor_logs=pd.DataFrame({"usuario":[]})
    if existe_csv:
        monitor_logs = pd.read_csv(ruta_logs_auditor_csv, sep=';')


    fecha_log_monitor=time.strftime("%Y-%m-%d %H:%M:%S")

    if not df_usuarios_modificados_sin_autorizacion.empty:
        for usuario in df_usuarios_modificados_sin_autorizacion["usuario"]:
            #solamente se imprimen a csv las modificaciones no reportadas
            if monitor_logs[monitor_logs["usuario"]==usuario].empty:
                mensaje= f' ALERTA: El usuario {usuario} fue editado sin autorizacion'
                existe_csv=os.path.exists(ruta_logs_auditor_csv)
                df_log = pd.DataFrame({'Fecha': [fecha_log_monitor],'Tipo_Alerta':'DETECTED_ATACK', 'usuario':usuario,'Mensaje': [mensaje]})
                df_log.to_csv(ruta_logs_auditor_csv, mode='a', header=not(existe_csv), index=False, sep=';')
                
       

try:
    while True:
        revision_edits_no_autorizados()
        time.sleep(2)

except KeyboardInterrupt:
    print("\nKeyboard interrupt received. Exiting...")




