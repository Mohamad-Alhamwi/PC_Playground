#!/bin/python3

from pwn import *

context.arch = 'amd64'

challenge_file = "CHALLENGE_PROCESS"
ps = process(challenge_file)
GREEN = "\033[92m"
RESET = "\033[0m"
flag = "KNOWN_PLAIN_TEXT"

# Fetch the encrypted fragment of the flag for the given length.
def get_flag_fragment(length):
    # Choose the option "Encrypt flag".
    ps.sendlineafter(b"Choice? ", str(2).encode())
    ps.sendlineafter(b"Index? ", str(0).encode())
    ps.sendlineafter(b"Length? ", str(length + 1).encode())

    line = ps.recvline().strip()
    flag_fragment = base64.b64decode(line.split(b"Result: ")[-1])

    # 'p' is at [0].
    # '}' is at [56]
    return flag_fragment

# Brute-force the flag character by character.
# by gradually building a flag fragment, incrementing the length as we discover new characters.
# We compare the entire fragment of the flag that we know (plus a new guessed character) against the encrypted version of the flag from the server.
def get_flag(flag):
    for length in range(len(flag), 57):
        # Loop through ASCII printable chars.
        for ascii_value in range(32, 127):
            # Choose the option "Encrypt chosen plaintext".
            ps.sendlineafter(b"Choice? ", str(1).encode())
            # Encrypt the flag + current guessed character.
            fragment = flag + chr(ascii_value)
            ps.sendlineafter(b"Data? ", fragment.encode())

            # Receive the encrypted fragment of the guessed flag.
            line = ps.recvline().strip()
            encrypted_fragment = base64.b64decode(line.split(b"Result: ")[-1])

            # Get the actual encrypted flag fragment from the server for comparison.
            flag_fragment = get_flag_fragment(length)

            # Compare the encrypted fragments: if they match, we found the correct character.
            if encrypted_fragment == flag_fragment:
                # Append the correct character to the flag.
                flag += chr(ascii_value)
                print(f"Found character: {chr(ascii_value)}")
                break
                
    return flag
        
flag = get_flag(flag)
print(f"\n{GREEN}The flag{RESET}:\n{flag}\n")
