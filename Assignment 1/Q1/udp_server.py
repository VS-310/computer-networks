from socket import socket, AF_INET, SOCK_DGRAM

# UDP server listening port
PORT = 12000

# Create UDP socket using IPv4
udp_server = socket(AF_INET, SOCK_DGRAM)

# Bind socket to all interfaces on the specified port
udp_server.bind(("", PORT))

print("UDP server running and waiting for messages")

while True:
    # Receive data and sender information
    data, sender_addr = udp_server.recvfrom(2048)

    # Decode incoming bytes and process message
    received_text = data.decode()
    response_text = received_text.upper()

    # Send processed data back to sender
    udp_server.sendto(response_text.encode(), sender_addr)
