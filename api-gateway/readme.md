# Instrucciones

## Software requerido

Instale lo siguiente:
• Node.js  - Sugerido v20.11.1
• npm - Sugerido v10.2.4 

Si esta en MacOS o Linux, asegurese de que Node y npm esté en el PATH y el PATH apunte a  /usr/local/bin
Si esta en Windows, asegurese de tener Node y npm de manera global y yambien esté en el path.

## Actualice o intslace las despendencias:
1. Abra su terminal de comandos.
2. Ubiquese en la raiz de este modulo.
3. Ejecute el siguiente comando:

```
npm install
```

## Ejecutar el API Gateway

1. Abra su terminal de comandos.
2. Ubiquese en la raiz de este modulo.
3. Ejecute el siguiente comando:

```
node gateway.js
```

Resultado:
```
[HPM] Proxy created: /  -> http://127.0.0.1:5000
Gateway running on port 3000
```

El servicio del API Gateway estará ahora en ejecución y escuchando en el puerto especificado.

## Ejecutar una solicitud OPERACION NORMAL

El API Gateway está ejecutándose en http://localhost:3000. Para enviar una solicitud al endpoint, puedes hacerlo usando herramientas como curl o  postman:

```curl
curl --location 'http://localhost:3000/api/v1/users' \
--header 'Content-Type: application/json' \
--data-raw '{
    "email": "armando.lios@yahoo.com"
}'
```

## Ejecutar una solicitud SIMULANDO FALLA a demanda

El API Gateway está ejecutándose en http://localhost:3000. Para enviar una solicitud simulando una falla a demanda al endpoint, puedes hacerlo usando herramientas como curl o  postman:

```curl
curl --location 'http://127.0.0.1:3000/api/v1/users' \
--header 'Content-Type: application/json' \
--data-raw '{
    "email": "jhon.puentes@yahoo.com",
    "simulate_failure": true,
    "failure_uuid": "c3582975-be19-47fd-8a16-cd0eb9533d7e"
}'
```

## Ejecutar una solicitud de PING-ECHO
El API Gateway está ejecutándose en http://localhost:3000. Para enviar una solicitud de MONITOREO con ping-echo al endpoint, puedes hacerlo usando herramientas como curl o  postman:

```curl
curl --location 'http://127.0.0.1:5000/ping'
```


## Notas
1. Puede requerir permisos de administrador o super usuario para ejecutar estos comandos.