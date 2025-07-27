from scapy.all import sniff, IP
from collections import defaultdict
from datetime import datetime, timedelta

# Thresholds for detection
MAX_PACKETS = 50
TIME_WINDOW = 10  # seconds

# Dictionary to track IPs and their packet timestamps
ip_activity = defaultdict(list)

# Dictionary to avoid logging the same IP repeatedly
last_alert_time = {}

# Time to wait before logging the same IP again (in seconds)
ALERT_COOLDOWN = 30

WHITELISTED_IPS = {"20.189.173.4", "192.168.1.1",
                   }


def packet_callback(packet):
    if IP in packet:
        src_ip = packet[IP].src
        dst_ip = packet[IP].dst
        now = datetime.now()

        # Add current timestamp to the IP's list
        ip_activity[src_ip].append(now)

        # Remove old timestamps
        ip_activity[src_ip] = [t for t in ip_activity[src_ip]
                               if (now - t).seconds < TIME_WINDOW]

        recent_count = len(ip_activity[src_ip])
        print(
            f"[{now.strftime('%H:%M:%S')}] {src_ip} → {dst_ip} | Count: {recent_count}")

        # Check threshold
        if recent_count > MAX_PACKETS:
            alert = f"{src_ip} is flooding the network with {recent_count} packets in {TIME_WINDOW}s!"
            print(f"🚨 ALERT: {alert}")

            # Avoid repeated logging for same IP in short time
            last_time = last_alert_time.get(src_ip)
            if not last_time or (now - last_time).seconds > ALERT_COOLDOWN:
                with open("alerts.log", "a") as f:
                    f.write(f"[{now}] ALERT: {alert}\n")
                last_alert_time[src_ip] = now
        if src_ip in WHITELISTED_IPS:
            return  # Skip processing


print("🧠 Smart Detector Started... (Ctrl+C to stop)")
sniff(prn=packet_callback, store=False)
