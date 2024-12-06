# De Jesus, Andrei Zarmin D. 
# Perez, Patrick Hans A.

import socket

HEADER = 512
FORMAT = 'utf-8'

IP_ADDRESS = "127.0.0.1"
PERMANENT_PORT = 12345  

def create_socket():
    return socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def display_commands():
    print("COMMAND LISTS")
    print("/join <server_ip_add> <port>")
    print("/leave")
    print("/register <handle>")
    print("/store <filename>")
    print("/dir")
    print("/get <filename>")

def send_to_server(client, msg):
    try:
        message = msg.encode(FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(FORMAT)
        send_length += b' ' * (HEADER - len(send_length))
        client.send(send_length)
        client.send(message)

        return client.recv(HEADER).decode(FORMAT)
    except (ConnectionResetError, ConnectionAbortedError, socket.error) as e:
        print(f"Error: Server connection lost. {e}")
        return None


def main():
    is_server_active = False
    is_user_registered = False
    print(IP_ADDRESS)
    client = create_socket()  # Create the socket initially

    input_server = ""
    input_port = -1

    while True:
        client_send_filename = ""
        client_receive_filename = ""

        prompt = input("> ")
        cmd_key = prompt.split()
        server_response = ""

        if cmd_key[0] == "/join":
            if len(cmd_key) == 3:
                input_server = cmd_key[1]  # a string
                input_port = int(cmd_key[2])  # an int
                address = (input_server, input_port)

            if input_port == PERMANENT_PORT and input_server == IP_ADDRESS and len(cmd_key) == 3 and is_server_active == False:
                is_server_active = True
                client.connect(address)
                server_response = send_to_server(client, prompt)
                print(server_response)
            elif input_port == PERMANENT_PORT and input_server == IP_ADDRESS and len(cmd_key) == 3 and is_server_active == True:
                print("Error: Connection to the Server is already active.")
            elif (input_port != PERMANENT_PORT or input_server != IP_ADDRESS) and len(cmd_key) == 3:
                print("Error: Connection to the Server has failed! Please check IP Address and Port Number.")
            else:
                print("Error: Command parameters do not match or are not allowed.")

        elif cmd_key[0] == "/leave":
            if is_server_active:
                server_response = send_to_server(client, prompt)
                if server_response is None:  # Server is unreachable
                    print("Error: Server connection lost.")
                else:
                    print(server_response)
                    if server_response == "Connection closed. Thank you!":
                        is_user_registered = False
                        is_server_active = False
                client.close()  # Close the socket
                client = create_socket()  # Recreate the socket for future use
            else:
                print("Error: Disconnection failed. Please connect to the server first.")

        elif cmd_key[0] in ["/store", "/dir", "/get"]:
            if is_server_active:
                if is_user_registered:
                    server_response = send_to_server(client, prompt)
                    if server_response is None:  # Server is unreachable
                        is_server_active = False
                        client.close()  # Close the socket
                        client = create_socket()  # Recreate the socket for future use
                        print("Error: Server connection lost.")
                    else:
                        print(server_response)
                else:
                    print("Error: User is not yet registered.")
            else:
                print("Error: Please connect to the server first to use this command.")

        elif cmd_key[0] == "/register":
            if len(cmd_key) != 2:
                print("Error: Command parameters do not match or are not allowed.")
            elif is_server_active:
                server_response = send_to_server(client, prompt)
                temp = server_response.split()
                if len(temp) == 2:
                    is_user_registered = True
                print(server_response)
            else:
                print("Error: Please connect to the server first to use this command.")

        elif cmd_key[0] == "/?":
            display_commands()

        elif cmd_key[0] == "/exit program":  # remove after testing
            break  # exit loop

        else:
            print("Error: Command not found.")


print("\nCLIENT INTERFACE")
print("> CLIENT HAS STARTED")
main()