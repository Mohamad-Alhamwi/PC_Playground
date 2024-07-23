from scapy.all import Ether, ARP, srp, sendp, sniff

def get_mac(dst_ip, interface):
    # Craft an ARP request to find the MAC address of the target IP
    arp_request = ARP(pdst=dst_ip)
    broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request

    # Send the packet and receive the response.
    responses, unanswered = srp(arp_request_broadcast, timeout = 2, retry = 1, verbose=True, iface = interface)

    # Extract the MAC address from the response.
    for response in responses:
        return response[1].hwsrc

    # If no response was received.
    return None

# Define required params.
interface = "eth0"
frame_type= 0xFFFF
dst_ip = "10.0.0.3"
dst_mac = get_mac(dst_ip, interface)
src_mac = "36:c4:4b:00:b8:bc"

if not dst_mac:
    print(f"No response received for IP {dst_ip}")

else:
    # Craft a frame.
    frame = Ether(src = src_mac, dst = dst_mac, type = frame_type)

    # Send the frame and receive the response.
    responses, unanswered = srp(frame, timeout = 2, retry = 1, verbose=True, iface = interface)

    for response in responses:
        print(response[1].hwsrc)
