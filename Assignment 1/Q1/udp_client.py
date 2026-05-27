from socket import socket, AF_INET, SOCK_DGRAM

# Address of the UDP server
SERVER_IP = "127.0.0.1"

# Port used by the UDP server
SERVER_PORT = 12000

# Create a UDP socket using IPv4
udp_client = socket(AF_INET, SOCK_DGRAM)

# Read message from user
text = input("Enter text: ")

# Close socket if no input is given
if not text:
    udp_client.close()
else:
    # Convert message to bytes and send to server
    udp_client.sendto(text.encode(), (SERVER_IP, SERVER_PORT))

    # Receive response from server
    reply, server_addr = udp_client.recvfrom(2048)

    # Decode and print server response
    print("Message from server:", reply.decode())

    # Close socket after communication
    udp_client.close()
