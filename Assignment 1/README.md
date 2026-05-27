## 1. Software and Network Requirements

* Python 3.x must be installed on the system
* Phone and PC should be connected to the same network for Q2
* Active internet connection is required for Q3

All implementations rely only on Python’s standard libraries.

---

## 2. Project Directory Layout

The files are organized as follows:

```
Q1/
   tcp_server.py
   tcp_client.py
   udp_server.py
   udp_client.py

Q2/
   udp_chat.py

Q3/
   mail_client.py
   sample.txt
```

---

## 3. Q1 - Client and Server Communication

Both TCP and UDP programs perform the same task: the client sends text and the server responds with the uppercase version.

### Running the UDP Version

1. Open a terminal window.
2. Start the UDP server:

   ```bash
   python udp_server.py
   ```
3. Open another terminal in the same directory and run:

   ```bash
   python udp_client.py
   ```
4. Type a message in the client terminal to see the server response.

---

### Running the TCP Version

1. Open a terminal.
2. Execute the TCP server first:

   ```bash
   python tcp_server.py
   ```
3. In a separate terminal, start the client:

   ```bash
   python tcp_client.py
   ```
4. Enter any text and observe the modified response returned by the server.

---

## 4. Q2 - UDP Chat Between Phone and PC

This program enables two-way communication between a mobile device and a PC using UDP.

1. Install the **UDP Monitor** application on the Android phone.
2. Ensure both devices are connected to the same WiFi network or hotspot.
3. Open UDP Monitor and note the following:

   * Phone IPv4 address
   * Port number configured in the app
4. On the PC, open Command Prompt.
5. Determine the PC’s IPv4 address:

   ```bash
   ipconfig
   ```

   Use the IPv4 address of the active network connection.
6. Edit `udp_chat.py` and update:

   * phone IP address
   * phone port number
7. Run the program on the PC:

   ```bash
   python udp_chat.py
   ```
8. Inside UDP Monitor:

   * Set Remote IP as the PC IPv4 address
   * Set Remote Port as the port used by the PC program
9. Messages can now be exchanged in both directions.

---

## 5. Q3 - SMTP Email Client

This section demonstrates sending an email using SMTP commands over a TCP connection.

1. Open `mail_client.py` and update:

   * sender email credentials
   * recipient addresses
2. Keep the attachment file in the same directory.
3. Execute:

   ```bash
   python mail_client.py
   ```
4. The program connects to the mail server and sends the email.


* Emails sent through SMTP may not always appear in the webmail Sent folder.

---