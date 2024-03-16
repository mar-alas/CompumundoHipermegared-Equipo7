# Microservicio para autenticación con segundo factor para deportista
Este es el repositorio de trabajo del equipo #7 para la asignatura de Arquitecturas Agiles de Software.

## Indice
* [Instrucciones Correr Programa](#instrucciones-programa)
* [Integrantes](#integrantes)
* [Modelo de componentes](#mod-componentes)

<a id="instrucciones-programa"></a>
## Instrucciones para correr programa

1. Realizar las configuraciones iniciales de los programas
2. Correr el api gateway
3. Correr el servicio de login

<a id="integrantes"></a>
## Integrantes


- Maria Alas
- Robert Castro
- Daniel Gamez
- Jhon Puentes

<a id="mod-componentes"></a>
## Modelo de componentes


![Diagramas_Sportapp_Seguridad-Componentes Equipo](https://github.com/mar-alas/CompumundoHipermegared-Equipo7/assets/142275813/7bdf83f3-02cd-4797-a91a-a58af4570679)



## API Gateway

El archivo `gateway.js` dentro del directorio `seguridad/api-gateway-service` es el punto de entrada principal del API Gateway.

### Requisitos Previos

Asegúrate de tener instalado [Node.js](https://nodejs.org/) en tu sistema para poder ejecutar el servicio. Este servicio ha sido probado en la versión de Node.js v18.

### Configuración y Ejecución

1. **Navega al Directorio del Servicio:**

   Abre una terminal y navega al directorio `seguridad/api-gateway-service`:

   ```bash
   cd seguridad/api-gateway-service
   ```

2. **Instalar dependencias:**

   ```bash
   npm install
   ```

3. **Iniciar servicio:**
  ```bash
    npm start
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
Navegue al director seguridad/microservicios/user_login/
Asegurese de tener el ambiente virtual de python activado (TODO como instalarlo y activarlo)
Iniciar la cola
```bash
celery -A queue_user_login worker --loglevel=info
```

### Actualizar el pythonpath
Agregar la carpeta de seguridad al python path con el siguiente comando:
export PYTHONPATH=$PWD/seguridad:$PYTHONPATH

### Rest API
Asegurese de tener el ambiente virtual de python activado 
Ejecute user_login_service.py (TODO hacer el de los datos del deportista y tener un api central)
```bash
python3.9 seguridad/microservicios/user_login/user_login_service.py
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

### Verificacion de politica de claves y validacion de datos para Login Service
El componente Login Data validator, valida lo siguiente:
* username debe ser un correo con sentido, valido y logico.
* el code 2FA, debe ser digitos y no debe superar 10 digitos.
* Politica segura para claves:
    Longitud mínima de 8 caracteres.
    Contiene letras mayúsculas y minúsculas, números y caracteres especiales.
    No utiliza información personal.
    No utiliza palabras comunes o secuencias alfabéticas o numéricas.

Para validar estas reglas de seguridad. Ejecute y pruebe:
```bash
curl --location 'http://127.0.0.1:5000/login' \
--header 'Content-Type: application/json' \
--data '{
    "username": "jhon@gmail.com",
    "password": "1234567",
    "code": ""
}'
```
Deberá obtener una respuesta asi:
```bash
{
    "message": "La contraseña debe contener al menos una letra mayúscula, una letra minúscula, un número y un carácter especial"
}
```

### Verificacion de certificados y validacion de datos al editar datos del usuario
Lo atacamos cuando
1. No enviamos los headers de certificacion.
2. No enviamos el certicicado que es.
3. No enviamos el keypass que es.
4. Enviamos un nombre corto (menos de 2 caracteres)
5. Enviamos un phone con tamaño distinto de 10 caracteres.

```bash
curl --location --request PUT 'http://127.0.0.1:5001/api/v1/users' \
--header 'X-certificate-data: 5d1c17c6-7d13-4d1e-8a36-5109a3e2c0d3' \
--header 'X-certificate-keypass: 1c476dcb-5911-4d03-b8a4-f293722fdcb2' \
--header 'Content-Type: application/json' \
--data '{
  "username": "12345",
  "name": "Jhon",
  "phone": "1234567890"
}'
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
