from dataclasses import dataclass


@dataclass
class PacketInfo:
    timestamp: str
    source_ip: str
    destination_ip: str

    source_port: int | None
    destination_port: int | None

    protocol: str
    packet_length: int

    tcp_flags: str | None

    def __str__(self):
        return (
            f"Time        : {self.timestamp}\n"
            f"Protocol    : {self.protocol}\n"
            f"Source      : {self.source_ip}:{self.source_port}\n"
            f"Destination : {self.destination_ip}:{self.destination_port}\n"
            f"Length      : {self.packet_length} bytes\n"
            f"TCP Flags   : {self.tcp_flags}\n"
            f"{'-'*45}"
        )