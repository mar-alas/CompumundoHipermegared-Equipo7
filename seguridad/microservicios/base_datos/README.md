# Base de Datos

La propuesta que les hago (DG) es guardar las tablas de la base de datos en formato csv dentro de esta carpeta. Centralizar aqui toda la data y tablas de logs.

* table_usuarios: tabla con el listado de usuarios con las columnas usuario, contrasenia y nombre. Las pruebas de edicion las propongo hacer sobre el campo nombre.

* table_login_logs: tabla donde se almacenan los logs del login. Por el momento desde el auditor de logins requiero que tenga fecha, usuario, y si el login fue exitoso o no.

* table_logs_login_audit_monitor: tabla donde se almacenan los logs del monitor de los logs del login. Por el momento tiene columnas:
    * Fecha
    * Tipo_Alerta
    * Mensaje

