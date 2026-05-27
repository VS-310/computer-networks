import socket
import ssl
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


# ================= MAIL SERVER SETTINGS =================
SMTP_HOST = "mmtp.iitk.ac.in"
SMTP_SSL_PORT = 465

RECV_BUFFER = 2048
# ========================================================


# ================= USER DETAILS =========================
SENDER_EMAIL = "sender@iitk.ac.in"
SENDER_PASSWORD = "*******"

TO_LIST = ["receiver2@iitk.ac.in"]
CC_LIST = ["copy@iitk.ac.in"]
BCC_LIST = [SENDER_EMAIL]

MAIL_SUBJECT = "(Test Email)"

MAIL_BODY = """Hello,

This mail is generated using a Python SMTP client.

Regards,
[****]
"""

FILE_TO_ATTACH = "sample.txt"
# ========================================================


# Receive response from SMTP server
def read_response(connection):
    reply = connection.recv(RECV_BUFFER).decode()
    print(reply)
    return reply


# Send command to SMTP server
def send_command(connection, cmd):
    print(">>", cmd)
    connection.send((cmd + "\r\n").encode())


def build_message():
    # Create MIME message container
    mail = MIMEMultipart()

    mail["From"] = SENDER_EMAIL
    mail["To"] = ", ".join(TO_LIST)
    mail["Cc"] = ", ".join(CC_LIST)
    mail["Subject"] = MAIL_SUBJECT

    # Attach text body
    mail.attach(MIMEText(MAIL_BODY, "plain"))

    # Add attachment if specified
    if FILE_TO_ATTACH:
        attachment = MIMEBase("application", "octet-stream")

        with open(FILE_TO_ATTACH, "rb") as file:
            attachment.set_payload(file.read())

        encoders.encode_base64(attachment)
        attachment.add_header(
            "Content-Disposition",
            f'attachment; filename="{FILE_TO_ATTACH}"'
        )

        mail.attach(attachment)

    return mail


def main():

    # Prepare MIME email
    email_message = build_message()

    # All recipients used in SMTP transaction
    all_receivers = TO_LIST + CC_LIST + BCC_LIST

    # Create SSL wrapped TCP socket
    ssl_context = ssl.create_default_context()
    smtp_socket = ssl_context.wrap_socket(
        socket.socket(socket.AF_INET, socket.SOCK_STREAM),
        server_hostname=SMTP_HOST
    )

    smtp_socket.connect((SMTP_HOST, SMTP_SSL_PORT))

    # Server greeting
    read_response(smtp_socket)

    # Identify client
    send_command(smtp_socket, "EHLO client")
    read_response(smtp_socket)

    # Authentication phase
    send_command(smtp_socket, "AUTH LOGIN")
    read_response(smtp_socket)

    send_command(
        smtp_socket,
        base64.b64encode(SENDER_EMAIL.encode()).decode()
    )
    read_response(smtp_socket)

    send_command(
        smtp_socket,
        base64.b64encode(SENDER_PASSWORD.encode()).decode()
    )
    read_response(smtp_socket)

    # Mail transaction
    send_command(smtp_socket, f"MAIL FROM:<{SENDER_EMAIL}>")
    read_response(smtp_socket)

    for receiver in all_receivers:
        send_command(smtp_socket, f"RCPT TO:<{receiver}>")
        read_response(smtp_socket)

    send_command(smtp_socket, "DATA")
    read_response(smtp_socket)

    smtp_socket.send(email_message.as_string().encode() + b"\r\n.\r\n")
    read_response(smtp_socket)

    # Terminate session
    send_command(smtp_socket, "QUIT")
    smtp_socket.close()

    print("Email has been sent successfully.")


if __name__ == "__main__":
    main()
