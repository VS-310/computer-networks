from socket import socket, AF_INET, SOCK_STREAM

# TCP server port number
PORT = 12111

# Create a socket for IPv4 using TCP protocol
tcp_server = socket(AF_INET, SOCK_STREAM)

# Attach the socket to the specified port
tcp_server.bind(("", PORT))

# Enable the server to accept incoming connections
tcp_server.listen(1)

print("Server is running and waiting for connections")

while True:
    # Accept a client connection
    # client_socket is used only for this connected client
    client_socket, client_address = tcp_server.accept()

    # Receive data sent by client
    data = client_socket.recv(2048)

    # Decode bytes to string
    received_text = data.decode()

    # Process message (convert to uppercase)
    response_text = received_text.upper()

    # Send processed message back to client
    client_socket.sendall(response_text.encode())

    # Close client connection after response
    client_socket.close()
