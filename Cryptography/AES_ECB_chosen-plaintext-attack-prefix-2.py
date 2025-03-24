#!/bin/python3

from pwn import *
from base64 import b64encode, b64decode

context.arch = 'amd64'

challenge_file = "CHALLENGE_FILE"
ps = process(challenge_file)
GREEN = "\033[92m"
RED = "\033[95m"
RESET = "\033[0m"

## The 5th Block starts showing up immediatly after 8th character.
## Flag length 57.

def optionOne(flag, ascii_value, length):
    ps.sendlineafter(b"Choice? ", str(1).encode())

    ## Encrypt the current guessed character + flag.
    fragment = chr(ascii_value) + flag
    
    ps.sendlineafter(b"Data? ", fragment.encode())

    ## Receive the encrypted fragment of the guessed flag.
    line = ps.recvline().strip()

    hex_temp_fragment = line.split(b'Result: ')[-1].decode()
    encrypted_temp_fragment = bytes.fromhex(hex_temp_fragment)[0:16]

    ## Flag Length: 16, Encrypted Length: 32.
    ## Flag Length: 32, Encrypted Length: 48.
    ## Flag Length: 48, Encrypted Length: 64.

    return encrypted_temp_fragment

def optionTwo(length):
    # Choose the option "Encrypt flag".
    ps.sendlineafter(b"Choice? ", str(2).encode())
    ps.sendlineafter(b"Data? ", b'A' * length)

    while True:
        line = ps.recvline().strip()
        if b"Result: " in line:
            hex_actual_fragment = line.split(b'Result: ')[-1].decode()
            encrypted_actual_fragment = bytes.fromhex(hex_actual_fragment)

            ## Slice to blocks.
            ## Always take the 5th block to compare with.
            encrypted_actual_fragment = encrypted_actual_fragment[64:80]

            break

    return encrypted_actual_fragment

def get_flag():
    flag = '}'

    for length in range(8 + len(flag), 65):

        # Loop through ASCII printable chars.
        for ascii_value in range(33, 127):

            # Get the temp encrypted flag fragment from the server for comparison.
            encrypted_temp_fragment = optionOne(flag, ascii_value, length)

            # Get the actual encrypted flag fragment from the server for comparison.
            encrypted_actual_fragment = optionTwo(length)

            # Compare the encrypted fragments: if they match, we found the correct character.
            if encrypted_temp_fragment == encrypted_actual_fragment:
                # Append the correct character to the flag.
                print(f"{RED}Found character: {chr(ascii_value)}{RESET}")
                flag = chr(ascii_value) + flag
                print(f"Flag Length: {len(flag)}")
                break

    return flag
      
def main():
    flag = get_flag()
    print(f"\n{GREEN}{flag}{RESET}\n")

if __name__ == "__main__":
    main()
