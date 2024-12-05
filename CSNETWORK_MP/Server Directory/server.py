import socket
import threading
import os
from pathlib import Path
import tqdm

HEADER = 512
PORT = 12345
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'

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
                file = open(cmd_key[1], "rb")
                file_size = os.path.getsize(cmd_key[1])
                
                conn.send(cmd_key[1].encode())
                conn.send(str(file_size).encode())
                
                data = file.read()
                conn.sendall(data)
                conn.send(b"<END>")
                
                file.close()
    
                conn.send("/store command received.".encode(FORMAT)) # send to client
            elif cmd_key[0] == "/dir":
                path = Path.cwd() / "CSNETWORK_MP" / "Server Directory"
                print(f"Server current working directory: {path}")  # Debugging

                files = list(path.glob("*"))  # Get all files
                if files:
                    print("Server Directory:")
                    for file in files:
                        print(file.name)
                    conn.send("\n".join([file.name for file in files]).encode(FORMAT))  # Send file names to client
                else:
                    print("No files found in the current directory.")
                    conn.send("No files found in the current directory.".encode(FORMAT))
                
            elif cmd_key[0] == "/get":
                # Implement logic for the /get command
                file_name = conn.recv(1024).decode()
                file_size = conn.recv(1024).decode()
                
                file = open(file_name, "wb")
                file_bytes = bytearray()
                done = False
                
                progress_bar = tqdm,tqdm(unit="B", unit_scale = True, unit_divisor=1000, total = int(file_size))
                
                while not done:
                    data = conn.recv(1024)
                    if data == file_size:
                        done = True
                    else:
                        file_bytes += data
                    progress_bar.update(1024)
                
                file.write(file_bytes)
                file.close()
                        
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
        