# Microservicio encargado de gestionar la creacion usuarios

## Ejecucion

### Rest API
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
```
celery -A user_registration_service_principal worker --loglevel=info
celery -A user_registration_service_redundancia1 worker --loglevel=info
celery -A user_registration_service_redundancia2 worker --loglevel=info
celery -A ping_service_log worker --loglevel=info
celery -A failures_with_user_registration_log worker --loglevel=info
```