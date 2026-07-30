from scapy.all import AsyncSniffer

from capture.analyzer import analyze_packet

from scapy.error import Scapy_Exception

from utils.logger import logger

from data.datastore import DataStore

class PacketCapture:
    """
    Handles live packet capture.
    """

    def __init__(self, interface="en0", packet_callback=None):
        self.interface = interface
        self.packet_callback =packet_callback
        self.is_running = False

        self.sniffer = None

    def process_packet(self, packet):
        """
        Called automatically whenever Scapy captures a packet.
        """
        packet_info = analyze_packet(packet)
        if self.packet_callback:
         self.packet_callback(packet_info) 

    def start(self):

     if self.is_running:

        #print("Capture is already running.")
        logger.warning("Capture is already running.")

        return

     try:

        self.sniffer = AsyncSniffer(

            iface=self.interface,

            prn=self.process_packet,

            store=False

        )

        self.sniffer.start()

        self.is_running = True

        #print(f"Started packet capture on {self.interface}")
        logger.info(f"Started packet capture on {self.interface}")

     except PermissionError:

        logger.error("ERROR: Permission denied.")

        logger.error("Try running the application with administrator privileges.")

     except Scapy_Exception as e:

        logger.error(f"ERROR: Scapy failed to start.\nReason: {e}")

     except Exception as e:

        logger.error(f"Unexpected error: {e}")

    
    def stop(self):

     if not self.is_running:
        logger.warning("Capture is not running.")
        return

     try:

        self.sniffer.stop()

        self.is_running = False

        #print("Packet capture stopped.")
        logger.info("Packet capture stopped.")

     except Exception as e:
        logger.error(f"Error while stopping capture: {e}")

data_store = DataStore()

def handle_packet(packet_info):
    data_store.add_packet(packet_info)
    
    # debugging console part
    # stats = data_store.get_statistics()
    # stats = data_store.get_statistics()
    # print("\n========== Statistics ==========")
    # for key, value in stats.items():
    #     print(f"{key}: {value}")

if __name__ == "__main__":

    capture = PacketCapture(
    packet_callback=handle_packet
)

    try:
        capture.start()

        input("\nPress ENTER to stop capture...\n")

    except KeyboardInterrupt:
        print("\nInterrupted by user.")

    finally:
        capture.stop()