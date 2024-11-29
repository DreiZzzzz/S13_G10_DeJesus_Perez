# imported python libraries
import socket 
import threading

HEADER = 128
FORMAT = 'utf-8'

def message(msg, client):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    print(client.recv(2048).decode(FORMAT))

def display_commands():
    print("COMMAND LISTS")
    print("(1) /join <server_ip_add> <port>")
    print("(2) /leave")
    print("(3) /register <handle>")
    print("(4) /store <filename>")
    print("(5) /get <filename>")
    
    
def main():
    
    while True:
        print("\n")
        user_input = input("> ")
        cmd = user_input.split()
        if cmd[0] == "/join":
            server = cmd[1]
            port = int(cmd[2])
            addr = (server, port)
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                client.connect(addr)
                message(user_input, client)
            except Exception as e:
                print(f"An error has occured. {e}.")
        elif cmd[0] == "/leave":
            message(cmd, client)
        elif cmd[0] == "/?": 
            display_commands()
        else:
            print("Error: Command not found.")


main()
                