# Microservicio para autenticación con segundo factor para deportista
Este es el repositorio de trabajo del equipo #7 para la asignatura de Arquitecturas Agiles de Software.

## Integrantes
- Maria Alas
- Robert Castro
- Daniel Gamez
- Jhon Puentes

## Modelo de componentes
![Diagramas_Sportapp_Seguridad-Componentes Equipo](https://github.com/mar-alas/CompumundoHipermegared-Equipo7/assets/142275813/7bdf83f3-02cd-4797-a91a-a58af4570679)



## API Gateway

El archivo `gateway.js` dentro del directorio `api-gateway-service` es el punto de entrada principal del API Gateway.

### Requisitos Previos

Asegúrate de tener instalado [Node.js](https://nodejs.org/) en tu sistema para poder ejecutar el servicio. Este servicio ha sido probado en la versión de Node.js v18.

### Configuración y Ejecución

1. **Navega al Directorio del Servicio:**

   Abre una terminal y navega al directorio `api-gateway-service`:

   ```bash
   cd api-gateway-service
   ```

2. **Instalar dependencias:**

   ```bash
   npm install
   ```

3. **Iniciar servicio:**
  ```bash
    npm start
  ```

### Verificación

**Verificar puerto de ejecución:**
  ```bash
    curl http://localhost:5000
  ```

### Verificación detección de Bots (Bot detector)

**Simulación request Google Bot:**
  ```bash
    curl -H "User-Agent: Googlebot/2.1 (+http://www.google.com/bot.html)" http://localhost:5000
  ```

### Verificación de IP (IP allow-list validator)

**IP Permitidas:**
  ```bash
    - IPv4 en IPv6 local: '::ffff:127.0.0.1'
    - IPv6 local: '::1'
  ```

### Verificación inyección SQL (SQL injection validator)

**Simulación request que incluye SQL:**
  ```bash
    curl -X POST http://localhost:5000 -d "usuario=' OR '1'='1' -- "
  ```

### Verificación XSS (Cross-Site Scripting validator)

**Simulación request que XSS**
  ```bash
    curl -X POST http://localhost:5000 -d "datos=<script>alert('XSS')</script>"
  ```

### Validación limitador de request para login (IP rate limiter)
1. **Renombra el archivo `.env.example` a `.env`**
2. **Ejecuta varios request al path login**
  ```bash
    curl -X POST http://localhost:5000/login
  ```

### Verificacion control de tamaño de la solicitud
Para comprobar el control de seguridad que se defiende de requests grandes en tamaño. Haga lo siguiente:
1. Dentro de la carpeta de microservicios, en cada servicio (user_login_service y user_editor_service) edite las lineas del tamaño maximo a permitir.
2. Editar los valores de la linea:
```python
app.config['MAX_CONTENT_LENGTH'] = 1 * 1 * 10
```
3. ejecute el siguente request:
```bash
curl --location 'http://127.0.0.1:5000/login' \
--header 'Content-Type: application/json' \
--data '{
    "username": "",
    "password": "",
    "code": ""
}'
```
Deberá obtener una respuesta de bloqueo asi:
```bash
{
    "message": "The data value transmitted exceeds the capacity limit."
}
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
```bash
docker run -p 6379:6379 -it redis/redis-stack:latest
```

## Iniciar Colas

### Colas 

```bash
celery -A queue_user_login worker --loglevel=info
```

## Correr el comando de curl para inicial sesion

### Comandos: 

Curl para ejecutar Login
```bash
curl --location 'http://127.0.0.1:5000/login' \
--header 'Content-Type: application/json' \
--data-raw '{
    "username": "maria",
    "password": "password1",
    "code": "1234"
}'
```