from socket import socket, AF_INET, SOCK_STREAM

# Address of the server (use IP or hostname)
SERVER_HOST = "127.0.0.1"

# Port number used by the TCP server
SERVER_PORT = 12111

# Create a TCP socket using IPv4
tcp_client = socket(AF_INET, SOCK_STREAM)

# Connect to the server
tcp_client.connect((SERVER_HOST, SERVER_PORT))

# Take input from user
user_text = input("Enter text: ")

# If input is empty, close connection and exit
if not user_text:
    tcp_client.close()
else:
    # Convert string to bytes and send to server
    tcp_client.sendall(user_text.encode())

    # Receive response from server
    server_reply = tcp_client.recv(2048)

    # Decode and print server response
    print("From Server:", server_reply.decode())

    # Close socket after communication
    tcp_client.close()
