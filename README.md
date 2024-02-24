# Microservicio para registro de usuarios en un sistema
Este es el repositorio de trabajo del equipo #7 para la asignatura de Arquitecturas Agiles de Software.

## Integrantes
- Maria Alas
- Robert Castro
- Daniel Gamez
- Jhon Puentes

## Ejecucion

### API gateway
Dentro del directorio /api-gateway ejecute:
```bash
node gateway.js
```

### Rest API
Dentro del directorio /user-registration-service ejecute
```bash
python3 create_new_user_rest_api.py 
```

### Inciar Docker Desktop o Docker Daemon
Inicie el proceso docker manual (Docker Desktop) o por comandos.
Guia: https://docs.docker.com/config/daemon/start/

### Iniciar servidor de Redis
```
docker run -p 6379:6379 -it redis/redis-stack:latest
```

## Iniciar Colas

### Colas del ping service

```
celery -A queue_ping_service_log worker --loglevel=info
celery -A queue_failures_ping_service_log worker --loglevel=info
```

### Colas del registro de usuarios
```
celery -A queue_user_registration_service_principal worker --loglevel=info
celery -A queue_user_registration_service_redundancia1 worker --loglevel=info
celery -A queue_user_registration_service_redundancia2 worker --loglevel=info
celery -A queue_failures_with_user_registration_log worker --loglevel=info
```

### TODO

1. *Hacer que el ping reciba el flag de failure y uuid.
2. Hacer la cola de eventos:
    2.1 Intento 1 de registro de usuario
    2.2 usuario registrado.
    2.3 Intento 2 de registro de usuario por redundancia 1
    2.4 intento de ping
    3.5 ping realizado
3. Hacer el reintento cuando se registra un primer fallo. Entonces llamar a la cola redundancia 1.
4. Hacer el reintento cuando se registra un segundo fallo. Entonces llamar a la cola redundancia 2.
5. Hacer cola de queries (aplicando chain, get result)
6. Crear cola de request and response
7. *Crear scripts de pyhton que hagan las invocaciones (y almacenar el request) al api gateway de forma masiva haciendo aleatorio el flag de falla y enviando el uuid.
    7.1 Hacer con ping (Maria)
    7.2 hacer con el api de registro - escribir en 2 archivo
8. Capturar fechas para medir tiempos de respuesta en:
    8.1 Desde cliente a servidor.
    8.2 de servidor a cola
    8.3 de cola a la BD