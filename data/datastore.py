import time
from collections import Counter

class DataStore:
    """
    Stores all captured packet information.
    """

    # ------------------ INITIALIZATION --------------------- 

    def __init__(self):
        self._initialize_packet_storage()
        self._initialize_statistics()
    
    def _initialize_packet_storage(self):
        self.packets = []

    def _initialize_statistics(self):
        self.protocol_counts = {
            "TCP": 0,
            "UDP": 0,
            "ICMP": 0,
            "ARP": 0,
            "OTHER": 0    
        }        

        self.total_packets = 0
        self.total_bytes = 0
        self.capture_start_time = time.time()
        self.source_ip_counts = Counter()
        self.destination_ip_counter = Counter()

# ------------------------ PACKET MANAGEMENT --------------------------=

    def add_packet(self, packet_info):
        """
        Store a captured packet.
        """
        self.packets.append(packet_info)
        protocol = packet_info.protocol
        if protocol in self.protocol_counts:
            self.protocol_counts[protocol]+=1
        else:
            self.protocol_counts["OTHER"]+=1   
        self.total_packets+=1
        self.total_bytes+=packet_info.packet_length
        self.source_ip_counts[packet_info.source_ip]+=1
        self.destination_ip_counter[packet_info.destination_ip] += 1


    def get_packets(self):
        """
        Return all stored packets.
        """
        return self.packets   
        
    def get_packet_count(self):
        """
        Return the total number of stored packets.
        """
        return len(self.packets)

    def clear(self):
        """
        Remove all stored packets.
        """
        self.packets.clear()

# ------------------------------ STATTISTICS -----------------------------------        
    
    def get_protocol_counts(self):
        """
        Return protocol statistics.
        """
        return self.protocol_counts

    def get_total_packets(self):
        return self.total_packets


    def get_total_bytes(self):
        return self.total_bytes


    def get_elapsed_time(self):
        return time.time() - self.capture_start_time

    def get_packet_rate(self):
        elapsed = self.get_elapsed_time()

        if elapsed==0:
            return 0
        else :
            return self.total_packets/elapsed

    def get_average_throughput(self):
        elapsed = self.get_elapsed_time()

        if elapsed ==0:
            return 0
        else:
            return self.total_bytes/ elapsed

    def get_top_source_ips(self, limit =5):
        return self.source_ip_counts.most_common(limit)    

    def get_top_destination_ips(self, limit=5):
        """
        Return the most active destination IPs.
        """
        return self.destination_ip_counter.most_common(limit)

    def get_statistics(self):
       """
       Return a snapshot of the current traffic statistics.
       """
       return {
           "total_packets": self.get_total_packets(),
           "total_bytes": self.get_total_bytes(),
           "packet_rate": self.get_packet_rate(),
           "average_throughput": self.get_average_throughput(),
           "protocol_counts": dict(self.get_protocol_counts()),
           "top_source_ips": list(self.get_top_source_ips()),
           "top_destination_ips": list(self.get_top_destination_ips()),
           "elapsed_time": self.get_elapsed_time(),
    }
    