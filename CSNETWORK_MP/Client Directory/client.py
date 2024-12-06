import socket

HEADER = 512
PERMANENT_PORT = 12345  # for checking
FORMAT = 'utf-8'

SERVER = "127.0.0.1"

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
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)

    return client.recv(HEADER).decode(FORMAT)


def main():
    is_server_active = False
    print(SERVER)
    client = create_socket()  # Create the socket initially

    input_server = ""
    input_port = -1

    while True:
        client_send_filename = ""
        client_receive_filename = ""

        prompt = input("> ")
        cmd_key = prompt.split()
        server_response = ""

        if cmd_key[0] == "/join" and is_server_active == False:
            if len(cmd_key) == 3:
                input_server = cmd_key[1]  # a string
                input_port = int(cmd_key[2])  # an int
                address = (input_server, input_port)

            if input_port == PERMANENT_PORT and input_server == SERVER and len(cmd_key) == 3:
                is_server_active = True
                client.connect(address)
                server_response = send_to_server(client, prompt)
                print(server_response)
            elif (input_port != PERMANENT_PORT or input_server != SERVER) and len(cmd_key) == 3:
                print("Error: Connection to the Server has failed! Please check IP Address and Port Number.")
            else:
                print("Error: Command parameters do not match or are not allowed.")

        elif cmd_key[0] == "/leave":
            if is_server_active:  # if true
                server_response = send_to_server(client, prompt)
                print(server_response)
                if server_response == "Connection closed. Thank you!":
                    is_server_active = False
                    client.close()  # Close the socket when leaving
                    client = create_socket()  # Recreate the socket for future use
            else:  # if false
                print("Error: Disconnection failed. Please connect to the server first.")

        elif cmd_key[0] in ["/register", "/store", "/dir", "/get"]:
            if is_server_active:
                print(send_to_server(client, prompt))
            else:
                print("Error: Please connect to the server first to use this command.") #

        elif cmd_key[0] == "/?":
            display_commands()

        elif cmd_key[0] == "/exit":  # remove after testing
            break  # exit loop

        else:
            print("Error: Command not found.")

        #print("\n")

print("\nCLIENT VIEW")
main()