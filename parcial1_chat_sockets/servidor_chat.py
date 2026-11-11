# Examen Parcial 1 - Servidor de chat en tiempo real con Sockets e Hilos.
# Acepta dos o mas clientes al mismo tiempo (un hilo por cliente) y
# difunde cada mensaje a todos los conectados. El servidor tambien
# participa en el chat desde su consola como [SERVIDOR].

import socket
import threading

# 0.0.0.0 permite aceptar conexiones desde fuera del contenedor Docker.
HOST = "0.0.0.0"
PORT = 5000

# Lista de clientes conectados. Varios hilos la leen y modifican
# al mismo tiempo, por eso su acceso se protege con un lock.
clientes = []
lock = threading.Lock()


def difundir(mensaje):
    # Envia el mismo mensaje a todos los clientes conectados.
    # Si un cliente ya se desconecto, se cierra y se quita de la lista.
    with lock:
        for conexion in list(clientes):
            try:
                conexion.sendall(mensaje)
            except (ConnectionError, OSError):
                try:
                    conexion.close()
                except OSError:
                    pass
                if conexion in clientes:
                    clientes.remove(conexion)


def atender_cliente(conexion, direccion):
    # Cada cliente se atiende en este hilo: sus mensajes llegan aqui
    # y se reenvian a todos los participantes del chat.
    with lock:
        clientes.append(conexion)

    print(f"Cliente conectado desde {direccion}")

    with conexion:
        try:
            # makefile convierte el socket en un canal de lineas:
            # readline() devuelve cada mensaje hasta el salto de linea.
            with conexion.makefile("rwb", buffering=0) as canal:
                # La primera linea que envia el cliente es su nombre:
                # es como se identificara en el chat.
                datos = canal.readline()
                if not datos:
                    with lock:
                        clientes.remove(conexion)
                    return
                nombre = datos.decode("utf-8").rstrip() or "CLIENTE"
                print(f"[SERVIDOR]: el cliente se registro como {nombre}")
                difundir(f"[SERVIDOR]: {nombre} se ha unido al chat\n".encode("utf-8"))

                while True:
                    datos = canal.readline()
                    if not datos:
                        break  # El cliente cerro la conexion.

                    mensaje = datos.decode("utf-8").rstrip()
                    print(f"[{nombre}]: {mensaje}")

                    # 'salir' cierra la conversacion con ese cliente
                    # (igual que en los ejercicios de clase).
                    if mensaje.strip().lower() == "salir":
                        difundir(f"[SERVIDOR]: Conexión finalizada.\n".encode("utf-8"))
                        break

                    difundir(f"[{nombre}]: {mensaje}\n".encode("utf-8"))
        except (ConnectionError, OSError):
            pass  # El cliente se desconecto de forma abrupta.

    # Al salir del bucle el cliente se fue: lo quitamos y lo avisamos.
    with lock:
        if conexion in clientes:
            clientes.remove(conexion)
    difundir(f"[SERVIDOR]: {nombre} salio del chat\n".encode("utf-8"))


def consola_servidor():
    # Difunde lo que el servidor escribe en su consola como [SERVIDOR].
    while True:
        try:
            texto = input()
        except EOFError:
            break
        if texto.strip():
            difundir(f"[SERVIDOR]: {texto}\n".encode("utf-8"))


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor:
    # SO_REUSEADDR evita el error "puerto en uso" al reiniciar rapido.
    servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    servidor.bind((HOST, PORT))
    servidor.listen()

    print(f"Servidor escuchando en {HOST}:{PORT}")
    print("Esperando conexiones de clientes...")

    # Hilo de consola para que el servidor tambien pueda chatear.
    threading.Thread(target=consola_servidor, daemon=True).start()

    while True:
        # accept() devuelve la conexion de un cliente nuevo.
        conexion, direccion = servidor.accept()

        # Cada cliente se atiende en un hilo independiente: asi los dos
        # conversan al mismo tiempo, sin esperar turnos.
        hilo = threading.Thread(
            target=atender_cliente,
            args=(conexion, direccion),
            daemon=True,
        )
        hilo.start()
