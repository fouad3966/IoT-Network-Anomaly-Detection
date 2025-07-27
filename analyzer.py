from scapy.all import sniff, IP, TCP, UDP
import csv
from datetime import datetime
import os

# Define the name of the CSV file to log packets
LOG_FILE = "packet_log.csv"

# If the file doesn't exist, create it with headers
if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, mode="w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Time", "Source IP", "Destination IP",
                        "Protocol", "Source Port", "Destination Port", "Length"])

# Define the callback for each captured packet


def packet_callback(packet):
    if IP in packet:
        ip_layer = packet[IP]
        src_ip = ip_layer.src
        dst_ip = ip_layer.dst
        proto = ip_layer.proto
        length = len(packet)

        # Default values
        src_port = dst_port = "-"

        # Identify protocol and get port numbers if applicable
        if TCP in packet:
            proto_name = "TCP"
            src_port = packet[TCP].sport
            dst_port = packet[TCP].dport
        elif UDP in packet:
            proto_name = "UDP"
            src_port = packet[UDP].sport
            dst_port = packet[UDP].dport
        else:
            proto_name = f"Other ({proto})"

        # Get timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Print summary in terminal
        print(
            f"[{timestamp}] {src_ip}:{src_port} → {dst_ip}:{dst_port} | {proto_name} | {length} bytes")

        # Save to CSV
        with open(LOG_FILE, mode="a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([timestamp, src_ip, dst_ip,
                            proto_name, src_port, dst_port, length])


# Start sniffing
print("📡 Packet analyzer started... Logging to 'packet_log.csv'")
sniff(prn=packet_callback, store=False)
