#!/bin/python3

from pwn import *

context.arch = 'amd64'

ps = process("CHALLENGE_FILES")

private_key = ""
public_key = ""
prime_num_p = ""
prime_num_q = ""
modules = ""
phi = ""
ciphertext = ""

# Get the required parameters from the process.
while True:
    line = ps.recvline().strip()
    
    if b"e: " in line:
        public_key = line.split(b"e: ")[-1]
        public_key = public_key.decode()
        public_key = int(public_key, 16)

    elif b"p: " in line:
        prime_num_p = line.split(b"p: ")[-1]
        prime_num_p = prime_num_p.decode()
        prime_num_p = int(prime_num_p, 16)
    
    elif b"q: " in line:
        prime_num_q = line.split(b"q: ")[-1]
        prime_num_q = prime_num_q.decode()
        prime_num_q = int(prime_num_q, 16)

    elif b"secret ciphertext (b64): " in line:
        ciphertext = line.split(b"secret ciphertext (b64): ")[-1]
        ciphertext = ciphertext.decode()
        ciphertext = base64.b64decode(ciphertext)
        ciphertext = int.from_bytes(ciphertext, "little")
        break

# Work out the modules.
modules = prime_num_p * prime_num_q

# Work out phi.
phi = (prime_num_p - 1) * (prime_num_q - 1)

# Work out the private key.
private_key = pow(public_key, -1, phi)

# Get the flag.
plaintext = pow(ciphertext, private_key, prime_num_p * prime_num_q).to_bytes(256, "little")
plaintext = plaintext.decode()
print(plaintext)
