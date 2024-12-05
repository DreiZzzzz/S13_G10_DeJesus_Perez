import socket
import threading

HEADER = 512
PORT = 12345
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

list_client_names = []  # Holds the list of names of active clients in the server

def handle_client(conn, addr):
    current_client = ""
    print(f"[NEW CONNECTION] {addr} connected") # prints to server interface

    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            cmd_key = msg.split()

            if cmd_key[0] == "/join":
                conn.send("Connection to the File Exchange Server is successful!".encode(FORMAT))
            elif cmd_key[0] == "/leave":
                connected = False
                conn.send("Connection closed. Thank you!".encode(FORMAT))
                if current_client != "":
                    list_client_names.remove(current_client)
            elif cmd_key[0] == "/register":
                # Check if cmd_key[1] is a valid name (non-empty)
                if len(cmd_key) > 1 and cmd_key[1]:
                    temp_client_name = cmd_key[1]
                    if temp_client_name not in list_client_names:
                        current_client = temp_client_name
                        list_client_names.append(current_client)
                        conn.send(f"Welcome {current_client}".encode(FORMAT))
                    else:
                        conn.send("Error: Registration failed. Handle or alias already exists.".encode(FORMAT))
            elif cmd_key[0] == "/store":
                # Implement logic for the /store command

                conn.send("/store command received.".encode(FORMAT)) # send to client
            elif cmd_key[0] == "/dir":
                # Implement logic for the /dir command

                conn.send("/dir command received.".encode(FORMAT)) # send to client
            elif cmd_key[0] == "/get":
                # Implement logic for the /get command

                conn.send("/get command received.".encode(FORMAT)) # send to client

            print(f"{addr}: {msg}")  # Optional, remove in production for cleaner output

    conn.close()


def start():
    server.listen()
    print(f"> SERVER HAS STARTED USING IP ADDRESS: {SERVER} ON PORT: {PORT}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}") # prints current active connection/s

print("\nSERVER VIEW")
start()
        