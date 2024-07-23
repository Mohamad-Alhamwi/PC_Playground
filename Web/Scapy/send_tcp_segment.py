from scapy.all import IP, TCP, sr1

# Define required params.
interface = "eth0"
protocol_type= 0x06
src_ip = "10.0.0.2"
dst_ip = "10.0.0.3"
src_port = 31337
dst_port = 31337
seq = 31337
ack = 31337
flags = "APRSF"

# Craft an IP packet.
ip_packet = IP(src = src_ip, dst = dst_ip, proto = protocol_type)

# Craft a TCP segment.
tcp_segment = TCP(sport = src_port, dport = dst_port, seq = seq, ack = ack, flags = flags)

# Craft a packet.
packet = ip_packet / tcp_segment

# Send the packet and receive the response.
response = sr1(packet, iface = interface)

# Print the response
if response:
    response.show()
else:
    print("No response received.")
