from scapy.all import Ether, IP, UDP, Raw, sendp, sniff
import sys

# Define a callback function to handle sniffed packets.
def packet_callback(packet):
    if UDP not in packet:
       return

    if packet[UDP].dport == 31337:
        print(packet)
    
        if Raw in packet:
            payload = packet[Raw].load.decode()
            print(" " + repr(payload))

            if payload == "ACTION?":
                    # Craft the response packet.
                    ether_frame = Ether(src = packet[Ether].dst, dst = packet[Ether].src)
                    ip_packet = IP(src = packet[IP].dst, dst = packet[IP].src)
                    udp_datagram = UDP(sport = packet[UDP].dport, dport = packet[UDP].sport)
                    my_payload = b"FLAG:10.0.0.1:31300\n"
                
                    # Encapsulate the different layers.
                    response_packet = ether_frame / ip_packet / udp_datagram / my_payload
                
                    # Send the packet.
                    sendp(response_packet, iface = interface)

interface = "eth0"
sniff(prn = packet_callback, iface = interface, filter = "", store = 0, timeout = 300)
