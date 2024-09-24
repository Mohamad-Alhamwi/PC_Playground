#!/bin/python3

from pwn import *
from Crypto.Hash.SHA256 import SHA256Hash

def brute_force(challenge):
    for num in range(1, 500000):
        response_raw = num.to_bytes(3, 'little')
        response_b64 = base64.b64encode(response_raw)
        hashed_value = SHA256Hash(challenge + response_raw).digest()

        if hashed_value[:2] == (b'\0' * 2):
            print(f"Response  (b64): {response_b64}")
            print(f"Hashed_value:    {hashed_value}")
            print(f"{GREEN}\n[+] Got a hit!{RESET}")
            print(f"{GREEN}[+] Response: {num}{RESET}\n")
            return response_b64
            
    return None

ps = process("CHALLENGE_FILE")
challenge= ""
GREEN = "\033[92m"
RESET = "\033[0m"

# Get the required parameters from the process.
while True:
    line = ps.recvline().strip()
    
    if b"challenge (b64): " in line:
        challenge_b64  = line.split(b"challenge (b64): ")[-1]
        print(f"\nChallenge (b64): {challenge_b64}")
        challenge_raw = base64.b64decode(challenge_b64)

        break

hit = brute_force(challenge_raw)

if not hit:
    print("No match found.\n")
    print("Aborted.\n")

ps.sendlineafter(b"response (b64): ", hit)

ps.interactive()
