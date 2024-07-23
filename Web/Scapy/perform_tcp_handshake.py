from scapy.all import IP, TCP, sr1

# Define required params.
interface = "eth0"
protocol_type= 0x06
src_ip = "10.0.0.2"
dst_ip = "10.0.0.3"
src_port = 31337
dst_port = 31337
seq = 31337
flags = "S"

# Craft an IP packet.
ip_packet = IP(src = src_ip, dst = dst_ip, proto = protocol_type)

# Craft a TCP segment.
tcp_segment = TCP(sport = src_port, dport = dst_port, seq = seq, flags = flags)

# Craft the initial packet.
initial_packet = ip_packet / tcp_segment

# Send the packet and receive the response.
response = sr1(initial_packet, iface = interface, verbose = False)

if response:
    print("SYN sent successfully.")

    # Craft a TCP segment with ack.
    seq = response[TCP].ack
    ack = response[TCP].seq + 1
    flags = "A"
    tcp_segment = TCP(sport = src_port, dport = dst_port, seq = seq, ack = ack, flags = flags)

    # Craft the packet.
    packet = ip_packet / tcp_segment

    # Send the packet and receive the response.
    response = sr1(packet, iface = interface, verbose = False)
    
    if response:
        print("Ack sent successfully.")
        response.show()

    else:
        print("No response (2) received.")

else:
    print("No response (1) received.")
