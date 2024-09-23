#!/bin/python3

from pwn import *
import itertools

context.arch = 'amd64'

ps = process("CHALLENGE_FILE")

def brute_force(secret_hash, max_length):
    charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789{}_."
    
    # Loop over possible lengths from 1 to max_length
    for length in range(1, max_length + 1):
        # Generate combinations of the specified length
        for attempt in itertools.product(charset, repeat=length):
            temp = ''.join(attempt)  # Create the string from the tuple
            # Hash the generated string
            hashed_temp = hashlib.sha256(temp.encode()).hexdigest()
            hashed_temp = hashed_temp[:4]
            print(hashed_temp)
            if hashed_temp == secret_hash:
                # Return the matched string if found.
                return temp
    return None

secret_hash = ""
GREEN = "\033[92m"
RESET = "\033[0m"

# Get the required parameters from the process.
while True:
    line = ps.recvline().strip()
    if b"secret sha256[:2] (b64): " in line:
        secret_hash = line.split(b"secret sha256[:2] (b64): ")[-1]
        secret_hash = secret_hash.decode()
        secret_hash = base64.b64decode(secret_hash)
        secret_hash = secret_hash.hex()

        break

hit = brute_force(secret_hash, 57)

if not hit:
    print("No match found.\n")
    print("Aborted.\n")

print(f"{GREEN}\n[+] Got a hit!{RESET}")
print(f"Collision value: {repr(hit)}\n")

ps.sendlineafter(b"collision (b64): ", base64.b64encode(f"{hit}".encode()))

ps.interactive()
