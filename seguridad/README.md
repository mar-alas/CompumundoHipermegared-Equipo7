# Microservicio para autenticación con segundo factor para deportista
Este es el repositorio de trabajo del equipo #7 para la asignatura de Arquitecturas Agiles de Software.

## Integrantes
- Maria Alas
- Robert Castro
- Daniel Gamez
- Jhon Puentes

## Modelo de componentes
![image](https://github.com/mar-alas/CompumundoHipermegared-Equipo7/assets/142593813/fa692d96-8da8-468b-afdc-459253d85f21)


## Ejecución

### API Gateway
Dentro del directorio /api-gateway-service ejecute:
```bash
node gateway.js
```

### Rest API
Dentro del directorio / ejecute
```bash
python3 auth_2fa.py 
```

### Inciar Docker Desktop o Docker Daemon
Inicie el proceso docker manual (Docker Desktop) o por comandos.
Guia: https://docs.docker.com/config/daemon/start/

### Iniciar servidor de Redis
```
docker run -p 6379:6379 -it redis/redis-stack:latest
```

## Iniciar Colas

### Colas 

```
celery -A 
celery -A 
```
