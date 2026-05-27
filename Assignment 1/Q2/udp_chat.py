from socket import socket, AF_INET, SOCK_DGRAM
import threading

# ================= SETTINGS =================
# IP address of mobile device running UDP Monitor
MOBILE_IP = "172.23.67.88"   # Update if phone IP changes

# Port configured inside UDP Monitor
MOBILE_PORT = 5005

# Local port used by PC to receive messages
LOCAL_PORT = 6006

# Maximum packet size
MAX_BUFFER = 2048
# ============================================

# Create UDP socket
udp_chat_socket = socket(AF_INET, SOCK_DGRAM)

# Bind socket so PC can receive incoming messages
udp_chat_socket.bind(("", LOCAL_PORT))

print("UDP chat session started")

# Thread function for receiving messages continuously
def receive_loop():
    while True:
        try:
            packet, sender = udp_chat_socket.recvfrom(MAX_BUFFER)
            print("\n[Phone]:", packet.decode())
            print("[Pc]: ", end="", flush=True)
        except:
            break

# Thread function for sending user input to phone
def send_loop():
    while True:
        try:
            text = input("[Pc]: ")
            udp_chat_socket.sendto(text.encode(), (MOBILE_IP, MOBILE_PORT))
        except:
            break

# Create threads for simultaneous send and receive
recv_thread = threading.Thread(target=receive_loop, daemon=True)
send_thread = threading.Thread(target=send_loop, daemon=True)

recv_thread.start()
send_thread.start()

# Keep program active while threads run
recv_thread.join()
send_thread.join()
