#!/bin/python3

from pwn import *

context.arch = 'amd64'

ps = process("CHALLENGE_FILE")

ciphertext = ""
private_key = ""
modules = ""

# Get the required parameters from the process.
while True:
    line = ps.recvline().strip()
    
    if b"d: " in line:
        private_key = line.split(b"d: ")[-1]
        private_key = private_key.decode()
        private_key = int(private_key, 16)
    
    elif b"n: " in line:
        modules = line.split(b"n: ")[-1]
        modules = modules.decode()
        modules = int(modules, 16)

    elif b"secret ciphertext (b64): " in line:
        ciphertext = line.split(b"secret ciphertext (b64): ")[-1]
        ciphertext = ciphertext.decode()
        ciphertext = base64.b64decode(ciphertext)
        ciphertext = int.from_bytes(ciphertext, "little")

        break

# Get the flag.
plaintext = pow(ciphertext, private_key, modules).to_bytes(256, "little")
print(repr(f"Flag: {plaintext.decode()}"))
