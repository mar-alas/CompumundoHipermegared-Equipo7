# Microservicio para registro de usuarios en un sistema
Este es el repositorio de trabajo del equipo #7 para la asignatura de Arquitecturas Agiles de Software.

## Integrantes
- Maria Alas
- Robert Castro
- Daniel Gamez
- Jhon Puentes

## Modelo de componentes
![image](https://github.com/mar-alas/CompumundoHipermegared-Equipo7/assets/142593813/fa692d96-8da8-468b-afdc-459253d85f21)


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
