# Examen Parcial 1 - Chat en tiempo real con Sockets, Hilos y Docker

Aplicacion de chat compuesta por un **servidor** (que corre dentro de un
contenedor Docker) y **dos clientes** (que corren en terminales de VS Code).
El servidor usa **sockets** e **hilos de ejecucion**: un hilo por cliente,
para que los participantes conversen al mismo tiempo, sin esperar turnos,
y difunde los mensajes entre todos.

## Participantes

- **Servidor**: recibe conexiones, envia mensajes y los distribuye entre los clientes.
- **Cliente 1**: envia y recibe mensajes.
- **Cliente 2**: envia y recibe mensajes.

## Requisitos

- Docker (Docker Desktop) instalado y en ejecucion.
- Python 3 para los clientes (no necesita librerias externas).
- Visual Studio Code con dos terminales.

## Como ejecutar la aplicacion

### 1. Iniciar el servidor dentro del contenedor Docker

Desde la carpeta del proyecto ejecutar:

```bash
docker compose up
```
### para escribir en el servidor se ejecuta el siguiente comando:

docker attach servidor_chat
```bash
Deberia verse:
```

```
Servidor de chat escuchando en 0.0.0.0:5000
Esperando conexiones de los clientes...
```

El `docker-compose.yml` publica el puerto **5000** del contenedor en el
puerto **5000** de la computadora anfitriona.

> Nota: en PowerShell usa `docker compose up` (con espacio). Si tu version de
> Docker es antigua, usa `docker-compose up`.

### 2. Conectar Cliente 1 desde una terminal de VS Code

Abrir una **primera terminal** en la carpeta del proyecto y ejecutar:

```bash
python cliente_chat.py
```

Cuando pida el nombre, escribir: `CLIENTE 1`

### 3. Conectar Cliente 2 desde otra terminal de VS Code

Abrir una **segunda terminal** (boton `+` en el panel de terminales) y ejecutar:

```bash
python cliente_chat.py
```

Cuando pida el nombre, escribir: `CLIENTE 2`

### 4. Chatear

- Escribir un mensaje en cualquier terminal y presionar **Enter**: el mensaje
  se difunde a todos los participantes.
- El servidor tambien puede escribir: en la terminal donde corre Docker,
  escribir un mensaje y presionar **Enter**, y los dos clientes lo recibiran.
- Para terminar un cliente escribir `salir`.

## Ejemplo de salida

```
[CLIENTE 1]: Hola a todos
[SERVIDOR]: Hola cliente 1
[CLIENTE 2]: Buenos dias
[CLIENTE 1]: ¿Como estan?
[CLIENTE 2]: Todo bien
```

## Archivos

| Archivo             | Descripcion                                                        |
| ------------------- | ------------------------------------------------------------------ |
| `servidor_chat.py`  | Servidor con sockets e hilos: difunde los mensajes a todos         |
| `cliente_chat.py`   | Cliente con hilos: envia y recibe mensajes a la vez                |
| `docker-compose.yml`| Ejecuta el servidor en Docker publicando el puerto 5000            |
| `README.md`         | Estas instrucciones                                                |
