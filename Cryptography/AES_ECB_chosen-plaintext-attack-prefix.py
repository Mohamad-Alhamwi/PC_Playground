#!/bin/python3

from pwn import *
from base64 import b64encode, b64decode

context.arch = 'amd64'

challenge_file = "CHALLENGE_FILE"
ps = process(challenge_file)
GREEN = "\033[92m"
RED = "\033[95m"
RESET = "\033[0m"

## The 5th Block starts showing up from the 8th character.
## Flag length 57.

def get_flag_fragment(length):
    # Choose the option "Encrypt flag".
    ps.sendlineafter(b"Choice? ", str(2).encode())
    ps.sendlineafter(b"Data? ", b'A' * length)

    while True:
        line = ps.recvline().strip()
        if b"Result: " in line:
            encoded_bytes = line.split(b'Result: ')[-1]
            ## Base64 deocode.
            decoded_bytes = b64decode(encoded_bytes)

            if length < 24:
                ## Slice to blocks then base64 encode it.
                flag_fragment = b64encode(decoded_bytes[64:]).decode()
            
            else:
                ## Slice to blocks then base64 encode it.
                flag_fragment = b64encode(decoded_bytes[64:80]).decode()

            break
            print(f"Flag Fragment: {flag_fragment}\n\n")        

    return flag_fragment

def get_flag(flag):
    for length in range(8 + len(flag), 65):
        # Loop through ASCII printable chars.
        for ascii_value in range(32, 127):
            # Choose the option "Encrypt chosen plaintext".
            ps.sendlineafter(b"Choice? ", str(1).encode())

            if length < 24:
                # Encrypt the current guessed character + flag.
                fragment = chr(ascii_value) + flag
                
            else:
                fragment = chr(ascii_value) + flag[0:15]
                print(f"Fragment: {fragment}")
            
            ps.sendlineafter(b"Data? ", fragment.encode())

            # Receive the encrypted fragment of the guessed flag.
            line = ps.recvline().strip()
            encrypted_temp_fragment = line.split(b'Result: ')[-1].decode()

            # Get the actual encrypted flag fragment from the server for comparison.
            encrypted_actual_fragment = get_flag_fragment(length)
            ## print(f"Encrypted Temp Fragment: {encrypted_temp_fragment}")

            # Compare the encrypted fragments: if they match, we found the correct character.
            if encrypted_temp_fragment == encrypted_actual_fragment:
                # Append the correct character to the flag.
                print(f"{RED}Found character: {chr(ascii_value)}{RESET}")
                flag = chr(ascii_value) + flag
                break

    return flag
      
def main():
    flag = "}"
    flag = get_flag(flag)
    print(f"\n{GREEN}{flag}{RESET}\n")

if __name__ == "__main__":
    main()
