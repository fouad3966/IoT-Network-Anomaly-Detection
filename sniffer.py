# Import the sniffing function from the Scapy networking library
from scapy.all import sniff

# This function will be called every time a packet is captured


def packet_callback(packet):
    # Check if the packet has an IP layer (to avoid crashing on non-IP traffic)
    if packet.haslayer('IP'):
        # Extract the IP layer from the packet
        ip_layer = packet['IP']
        # Print the source and destination IP addresses + the protocol number
        print(f"[+] {ip_layer.src} → {ip_layer.dst} | Protocol: {ip_layer.proto}")


# Print a startup message
print("🔍 Starting packet capture... (Press Ctrl+C to stop)")

# Start sniffing packets:
# - prn=packet_callback means: call our function on every packet
# - store=False means: don’t save packets in memory (saves RAM)
sniff(prn=packet_callback, store=False)
