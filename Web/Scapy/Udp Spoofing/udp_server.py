#!/usr/bin/python3

import socket
import time

receiving_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
my_socket = ("10.0.0.1", 31300)
receiving_socket.bind(my_socket)

print(f"Listening on {my_socket[0]}:{my_socket[1]}")
while True:
    data, addr = receiving_socket.recvfrom(1024)
    print(f"Received s response: {data}")
