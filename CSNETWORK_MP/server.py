import socket 
import threading

HEADER = 128
PORT = 12345
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

#Notes
# socket.gethostname() => Andrei 
# socket.gethostbyname(socket.gethostname()) => IPV4 address

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR) 

clients = []

def print_ast():
    print("****************************************************")

def handle_commands(msg, conn):
    cmd = msg.split()
    
    if cmd == "/register":
        conn.send("!".encode(FORMAT)")
    
    

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected")
    
    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        print(msg_length)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                connected = False
                
            print(f"{addr}: {msg}")
            
            if msg == "\?":
                print()
                
        conn.send("Connection to the File ExchangeServer is successful!".encode(FORMAT))

        
    conn.close()

def start():
    server.listen()
    print(f"Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")
        print(f"Connection to the File ExchangeServer is successful!")

print("STARTING. Server is starting...")

start()
        