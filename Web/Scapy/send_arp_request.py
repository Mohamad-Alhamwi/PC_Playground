from scapy.all import Ether, ARP, srp

# Define required params.
interface = "eth0"
operation = "is-at"
src_mac = "10.0.0.2"
dst_ip = "10.0.0.3"
src_mac = "46:e9:55:93:81:53"
dst_mac = "ff:ff:ff:ff:ff:ff"

# Craft an ARP packet.
arp_request = ARP(pdst = dst_ip, op = operation)
ether_frame = Ether(src = src_mac, dst = dst_mac)
arp_packet = ether_frame / arp_request

# Send the packet and receive the response.
responses, unanswered = srp(arp_packet, timeout = 2, retry = 1, verbose=True, iface = interface)

if responses:
    for response in responses:
        print(response[1].hwsrc)

else:
    print(f"No response received for IP {dst_ip}")
