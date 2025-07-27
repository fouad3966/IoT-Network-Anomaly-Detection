from scapy.all import sniff, IP, TCP, UDP
import pandas as pd
from datetime import datetime
from collections import defaultdict

# Parameters
capture_duration = 20  # seconds
interface = None  # or "eth0", "Wi-Fi", etc.

# Packet storage
packets_by_second = defaultdict(list)

# Packet handler


def process_packet(packet):
    if IP in packet:
        timestamp = datetime.fromtimestamp(packet.time)
        key = timestamp.replace(microsecond=0)  # group by second
        packets_by_second[key].append(packet)


# Start sniffing
print("📡 Capturing packets...")
sniff(prn=process_packet, timeout=capture_duration, iface=interface)
print("✅ Capture complete.")

# Process features
feature_rows = []
for ts, packets in packets_by_second.items():
    packet_count = len(packets)
    total_size = sum(len(pkt) for pkt in packets)
    tcp_count = sum(1 for pkt in packets if TCP in pkt)
    udp_count = sum(1 for pkt in packets if UDP in pkt)
    avg_packet_size = total_size / packet_count if packet_count > 0 else 0

    # Rule-based anomaly label
    is_anomaly = 1 if packet_count > 30 or avg_packet_size > 1000 else 0

    feature_rows.append({
        'second_frame': ts,
        'packet_count': packet_count,
        'avg_packet_size': round(avg_packet_size, 2),
        'tcp_count': tcp_count,
        'udp_count': udp_count,
        'is_anomaly': is_anomaly
    })

# Convert to DataFrame and save
df = pd.DataFrame(feature_rows)
df.to_csv("labeled_traffic.csv", index=False)
print("📄 Saved labeled features to labeled_traffic.csv")
