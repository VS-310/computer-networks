# Computer Networks

A collection of three networking assignments covering socket programming, protocol analysis, and routing algorithms.

---

## Repository Structure

```
networks/
├── Assignment 1/          # Socket programming (TCP, UDP, SMTP)
│   ├── Assignment1.pdf
│   ├── README.md
│   ├── Q1/
│   │   ├── tcp_client.py
│   │   ├── tcp_server.py
│   │   ├── udp_client.py
│   │   └── udp_server.py
│   ├── Q2/
│   │   └── udp_chat.py
│   └── Q3/
│       ├── mail_client.py
│       └── sample.txt
│
├── Assignment 2/          # Wireshark, NetSim, iPerf analysis
│   ├── Assignment2.pdf
│   ├── README.md
│   ├── README.pdf
│   └── report.pdf
│
└── Assignment 3/          # Routing algorithms & HOL blocking
    ├── Assignment3.pdf
    ├── part1_q2.py
    ├── part2_q2.py
    ├── q3.py
    ├── README.pdf
    └── report.pdf
```

---

## Assignment 1: Socket Programming

Implements client-server communication using TCP and UDP sockets, a UDP-based cross-device chat, and a raw SMTP email client.

### Q1 : TCP and UDP Echo Servers

Both programs send a text string to a server and receive it back in uppercase.

**UDP**

```bash
# Terminal 1
python udp_server.py

# Terminal 2
python udp_client.py
```

**TCP**

```bash
# Terminal 1
python tcp_server.py

# Terminal 2
python tcp_client.py
```

| File | Port | Protocol |
|------|------|----------|
| `udp_server.py` / `udp_client.py` | 12000 | UDP |
| `tcp_server.py` / `tcp_client.py` | 12111 | TCP |

### Q2 : UDP Chat (PC ↔ Android Phone)

Two-way real-time messaging between a PC and a mobile device over UDP.

**Setup**

1. Install the **UDP Monitor** app on the Android device.
2. Connect both devices to the same Wi-Fi network.
3. Note the phone's IPv4 address and the port configured in UDP Monitor.
4. Find the PC's IPv4 address:
   ```bash
   ipconfig      # Windows
   ip a          # Linux/macOS
   ```
5. Edit `udp_chat.py` and update `MOBILE_IP` and `MOBILE_PORT`.
6. Run on PC:
   ```bash
   python udp_chat.py
   ```
7. In UDP Monitor, set Remote IP → PC's IPv4, Remote Port → `6006`.

### Q3 : SMTP Email Client

Sends an email with an attachment directly over a raw TCP/SSL socket using SMTP commands (no `smtplib`).

**Setup**

1. Open `mail_client.py` and update `SENDER_EMAIL`, `SENDER_PASSWORD`, `TO_LIST`, `CC_LIST`, and `FILE_TO_ATTACH`.
2. Place the attachment file in the same directory.
3. Run:
   ```bash
   python mail_client.py
   ```

> **Note:** Emails sent via raw SMTP may not appear in the webmail Sent folder.

---

## Assignment 2: Protocol Analysis

Experimental analysis using Wireshark, NetSim, and iPerf. No source code, results are documented in `report.pdf`.

### Q1 : Wireshark: TCP and UDP Analysis

**TCP capture steps:**
1. Start Wireshark and begin capturing on the active interface.
2. Download `http://gaia.cs.umass.edu/wireshark-labs/alice.txt` in a browser.
3. Upload the file to `http://gaia.cs.umass.edu/wireshark-labs/TCP-wireshark-file1.html`.
4. Stop the capture once the upload succeeds.

Useful display filters:

```
tcp                                          # all TCP traffic
tcp.flags.syn == 1 && tcp.flags.ack == 0    # client SYN
tcp.flags.syn == 1 && tcp.flags.ack == 1    # server SYN-ACK
http.request.method == "POST"               # HTTP POST
tcp.analysis.retransmission                 # retransmissions
udp                                         # UDP packets
```

**UDP capture:** Use the trace file `http-ethereal-trace-5` or capture live DNS/SNMP traffic.

### Q2 : NetSim: TCP Congestion Control

Compares **TCP Old Tahoe**, **Reno**, and **Cubic** over a lossy wired link.

Topology: `Client ── (10 Mbps, BER 1e-7, 25 ms delay) ── Server`

| Parameter | Value |
|-----------|-------|
| Bandwidth | 10 Mbps |
| BER | 1e-7 |
| Propagation delay | 25 ms |
| MSS | 1460 bytes |
| Application | FTP, 100 MB file |
| Simulation time | 20 s |

Run three simulations (one per TCP variant) with Wireshark capture enabled. Plot congestion window via **Statistics → TCP Stream Graph**.

### Q3 : iPerf: Bandwidth Measurement

```bash
# Machine A (server)
iperf3 -s -p <port>

# Machine B (client) - forward test
iperf3 -c <server_ip> -p <port>

# Machine B - reverse test
iperf3 -c <server_ip> -p <port> -R
```

---

## Assignment 3: Routing Algorithms & HOL Blocking

### Network Topology (Q2)

```
0 --1-- 1
|  \    |
7   3   1
|    \  |
3 --2-- 2
```

Edge weights represent link costs.

### Q2 Part 1 : Link-State Routing (Dijkstra's Algorithm)

Runs Dijkstra's algorithm from every node and prints the shortest-path cost vector and routing table for each source.

```bash
python part1_q2.py
```

**Sample output:**
```
Node 0 : Dijkstra's Algorithm Results
  Destination     Cost       Next Hop
  1               1          1
  2               2          1
  3               4          1
```

### Q2 Part 2 : Distance-Vector Routing (Bellman-Ford)

Simulates the distributed Bellman-Ford algorithm with packet-passing between nodes until convergence.

```bash
python part2_q2.py
```

Displays the distance table at each node after every update, and prints final routing tables once the algorithm converges.

### Q3 : Head-of-Line (HOL) Blocking Analysis

Models a 2×2 packet switch as a Markov chain and computes the stationary distribution and throughput using three independent methods:

| Method | Description |
|--------|-------------|
| Analytical | Solve `πP = π` as a linear system |
| Power iteration | Compute `P^1000` |
| Monte Carlo | Simulate 1,000,000 time steps |

```bash
python q3.py
```

**Key result:** Under HOL blocking, switch efficiency is approximately **75%** (1.5 packets/slot vs. the ideal 2.0 packets/slot).

---

## Requirements

| Assignment | Dependencies |
|------------|-------------|
| Assignment 1 | Python 3.x - standard library only |
| Assignment 2 | Wireshark, NetSim, iPerf3 |
| Assignment 3 | Python 3.x, NumPy (`pip install numpy`) |

All Assignment 1 and 3 scripts use only standard library or NumPy, no additional setup required beyond a working Python 3 installation.
