#!/bin/python3

from pwn import *
from Crypto.PublicKey import RSA

context.arch = 'amd64'

def encrypt_RSA(plaintext, private_key, modules):
    print(f"{GREEN}\nRSA encryption has started.\n{RESET}")
    ciphertext = pow(plaintext, private_key, modules)
    
    return ciphertext

def decrypt_RSA(ciphertext, public_key, modules):
    print(f"{GREEN}\nRSA decryption has started.\n{RESET}")
    plaintext = pow(ciphertext, public_key, modules)

    return plaintext

ps = process("CHALLENGE_FILE")
key = RSA.generate(1024)
GREEN = "\033[92m"
RESET = "\033[0m"

public_key = key.e
private_key = key.d
modules = key.n
challenge = ""
secret = ""
flag = ""

ps.sendlineafter(b"e: ", hex(public_key).encode())
ps.sendlineafter(b"n: ", hex(modules).encode())

# Get the required parameters from the process.
while True:
    line = ps.recvline().strip()
    if b"challenge: " in line:
        challenge = line.split(b"challenge: ")[-1]
        challenge = challenge.decode()
        challenge = int(challenge, 16)
        break

encrypted_response = encrypt_RSA(challenge, private_key, modules)
encrypted_response_hex = hex(encrypted_response)
ps.sendlineafter(b"response: ", encrypted_response_hex.encode())

line = ps.recvline().strip()
secret = line.split(b"secret ciphertext (b64): ")[-1]
secret_raw = base64.b64decode(secret)
secret_int = int.from_bytes(secret_raw, 'little')
flag_int = decrypt_RSA(secret_int, private_key, modules)
flag_raw = flag_int.to_bytes(256, "little").rstrip(b"\x00")
flag = flag_raw.decode()
print(f"Flag: {flag}")

ps.interactive()
