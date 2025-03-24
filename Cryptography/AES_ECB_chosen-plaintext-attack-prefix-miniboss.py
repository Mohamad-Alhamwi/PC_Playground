#!/bin/python3

from pwn import *

context.arch = 'amd64'

challenge_file = "CHALLENGE_FILE"
ps = process(challenge_file)
GREEN = "\033[92m"
RED = "\033[95m"
RESET = "\033[0m"

def main():
    flag = ''
    print("\n")

    ## The 5th block starts showing up at the 7th character, but you need to account for the padding block so start from the 8th one.
    for counter in range(8, 65):
        # Loop through ASCII printable chars.
        for ascii_value in range(33, 127):
            block_size = 16
            prefix = b'A' * counter

            if len(flag) < 16:
                fragment = chr(ascii_value) + flag
            
            else:
                fragment = chr(ascii_value) + flag[0:15]

            pad_len = block_size - len(fragment)
            my_input = fragment.encode() + (bytes([pad_len]) * pad_len) + prefix
            my_hex_input = my_input.hex()
            ps.sendlineafter(b"Data? ", my_hex_input.encode())

            ## Receive the encrypted flag.
            line = ps.recvline().strip()
            hex_temp_fragment = line.split(b'Ciphertext: ')[-1].decode().strip()

            blocks = [hex_temp_fragment[i:i+32] for i in range(0, len(hex_temp_fragment), 32)]
            if blocks[0] == blocks[5]:
                print(f"{RED}Found Character: {chr(ascii_value)}{RESET}")
                flag = chr(ascii_value) + flag
    
    print(f"\n{GREEN}{flag}{RESET}\n")

if __name__ == "__main__":
    main()
