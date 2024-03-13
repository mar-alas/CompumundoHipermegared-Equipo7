# Microservicio para autenticación con segundo factor para deportista
Este es el repositorio de trabajo del equipo #7 para la asignatura de Arquitecturas Agiles de Software.

## Integrantes
- Maria Alas
- Robert Castro
- Daniel Gamez
- Jhon Puentes

## Modelo de componentes
![Diagramas_Sportapp_Seguridad-Componentes Equipo](https://github.com/mar-alas/CompumundoHipermegared-Equipo7/assets/142275813/7bdf83f3-02cd-4797-a91a-a58af4570679)



## Ejecución

### API Gateway
Dentro del directorio /api-gateway-service ejecute:
```bash
npm install
```
y luego
```bash
npm start
```

### Rest API
Dentro del directorio /seguridad ejecute (paso 2: hacer el de los datos del deportista y tener un api central)
```bash
python3.9 microservicios/user_login/user_login_service.py
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
celery -A queue_user_login worker --loglevel=info
celery -A 
```

## Correr el comando de curl para inicial sesion

### Comandos: 
curl --location 'http://127.0.0.1:5000/login' \
--header 'Content-Type: application/json' \
--data-raw '{
    "username": "maria",
    "password": "password1",
    "code": "1234"
}'