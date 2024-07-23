from scapy.all import sr1, IP

# Define required params.
interface = "eth0"
protocol_type= 0xFF
src_ip = "10.0.0.2"
dst_ip = "10.0.0.3"

# Craft a packet.
packet = IP(src = src_ip, dst = dst_ip, proto = protocol_type)

# Send the packet and receive the response.
response = sr1(packet)

# Print the response
if response:
    response.show()
else:
    print("No response received.")
