# Examen Parcial 1 - Cliente de chat en tiempo real con Sockets e Hilos.
# Envia y recibe mensajes al mismo tiempo, sin esperar turnos.
# Ejecutar en dos terminales de VS Code: python cliente_chat.py

import socket
import threading

# Direccion del servidor publicado por Docker en la computadora anfitriona.
HOST = "127.0.0.1"
PORT = 5000


def recibir(cliente):
    # Hilo que imprime todo lo que llega de los demas participantes.
    with cliente.makefile("rb") as canal:
        while True:
            datos = canal.readline()
            if not datos:
                print("Servidor desconectado.")
                cliente.close()
                return
            print(datos.decode("utf-8").rstrip())


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cliente:
    cliente.connect((HOST, PORT))

    # El nombre identifica al participante ([CLIENTE 1], [CLIENTE 2], ...).
    nombre = input("Tu nombre (ej. CLIENTE 1): ").strip() or "CLIENTE"

    # La primera linea que enviamos es el nombre: el servidor lo usa
    # para identificar todos nuestros mensajes en el chat.
    cliente.sendall(f"{nombre}\n".encode("utf-8"))

    print(f"Conectado al servidor {HOST}:{PORT} como {nombre}")
    print("Escribe mensajes. Escribe 'salir' para terminar.")

    # El hilo receptor empieza de inmediato: mientras escribimos
    # en el bucle de abajo, los mensajes recibidos se van imprimiendo.
    threading.Thread(target=recibir, args=(cliente,), daemon=True).start()

    while True:
        try:
            mensaje = input()
        except EOFError:
            break

        # El mensaje viaja con salto de linea: es el delimitador que
        # el servidor usa con readline() para saber donde termina.
        cliente.sendall(f"{mensaje}\n".encode("utf-8"))

        if mensaje.strip().lower() == "salir":
            break
