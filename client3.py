import socket

# Server Configuration
SERVER_IP = "127.0.0.1"  # Change this to the server's IP
PORT = 12345

# Connect to the server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_IP, PORT))

message=client_socket.recv(1024).decode()
print(message)
message=client_socket.recv(1024).decode()
print(message)

# Game loop
while True:
    message = client_socket.recv(1024).decode()
    print(message)
    inp=input("Enter : ")
    client_socket.send(inp.encode())
    message = client_socket.recv(1024).decode()
    print(message)
    message = client_socket.recv(1024).decode()
    print(message)

##    if "Your turn" in message:
##        guess = input("Enter your guess: ")
##        client_socket.send(guess.encode())
##
##    if "win" in message or "lost" in message:
##        break  # Game over

# Close socket
client_socket.close()
