from datetime import datetime

from scapy.layers.inet import IP, TCP, UDP, ICMP
from scapy.layers.l2 import ARP

from data.packet import PacketInfo


def analyze_packet(packet):

    timestamp = datetime.now().strftime("%H:%M:%S")

    source_ip = "N/A"
    destination_ip = "N/A"

    source_port = None
    destination_port = None

    protocol = "Other"

    tcp_flags = None

    if packet.haslayer(IP):

        source_ip = packet[IP].src
        destination_ip = packet[IP].dst

        if packet.haslayer(TCP):

            protocol = "TCP"

            source_port = packet[TCP].sport
            destination_port = packet[TCP].dport

            tcp_flags = packet[TCP].sprintf("%TCP.flags%")

        elif packet.haslayer(UDP):

            protocol = "UDP"

            source_port = packet[UDP].sport
            destination_port = packet[UDP].dport

        elif packet.haslayer(ICMP):

            protocol = "ICMP"

        else:

            protocol = "IP"

    elif packet.haslayer(ARP):

        protocol = "ARP"

        source_ip = packet[ARP].psrc
        destination_ip = packet[ARP].pdst

    packet_length = len(packet)

    return PacketInfo(
        timestamp=timestamp,
        protocol=protocol,
        source_ip=source_ip,
        destination_ip=destination_ip,
        source_port=source_port,
        destination_port=destination_port,
        packet_length=packet_length,
        tcp_flags=tcp_flags
    )