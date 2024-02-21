# Microservicio encargado de gestionar la creacion usuarios

## Ejecucion

### Rest API
```bash
python3 create_new_user_rest_api.py 
```

### Iniciar servidor de Redis
```
docker run -p 6379:6379 -it redis/redis-stack:latest
```

## Iniciar Colas
```
celery -A user_registration_service_principal worker --loglevel=info
celery -A user_registration_service_redundancia1 worker --loglevel=info
celery -A user_registration_service_redundancia2 worker --loglevel=info
```