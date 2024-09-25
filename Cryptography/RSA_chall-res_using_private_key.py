#!/bin/python3

from pwn import *

context.arch = 'amd64'

def encrypt_RSA(plaintext, private_key, modules):
    print(f"{GREEN}\nRSA encryption has started.\n{RESET}")
    ciphertext = pow(plaintext, private_key, modules)

    return ciphertext

ps = process("/challenge/run")
public_key = ""
private_key = ""
modules = ""
challenge = ""
GREEN = "\033[92m"
RESET = "\033[0m"

# Get the required parameters from the process.
while True:
    line = ps.recvline().strip()
    if b"e: " in line and b"challenge:" not in line:
        public_key = line.split(b"e: ")[-1]
        public_key = public_key.decode()
        public_key = int(public_key, 16)

    elif b"d: " in line:
        private_key = line.split(b"d: ")[-1]
        private_key = private_key.decode()
        private_key = int(private_key, 16)
    
    elif b"n: " in line:
        modules = line.split(b"n: ")[-1]
        modules = modules.decode()
        modules = int(modules, 16)

    elif b"challenge: " in line:
        challenge = line.split(b"challenge: ")[-1]
        challenge = challenge.decode()
        challenge = int(challenge, 16)

        break

encrypted_response = encrypt_RSA(challenge, private_key, modules)
encrypted_response_hex = hex(encrypted_response)

ps.sendlineafter(b"response: ", encrypted_response_hex.encode())

ps.interactive()
