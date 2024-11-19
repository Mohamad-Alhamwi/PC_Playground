#!/bin/python3

from pwn import *

context.arch = 'amd64'

challenge_file = "CHALLENGE_FILE"
ps = process(challenge_file)
GREEN = "\033[92m"
RESET = "\033[0m"
temp_flag = "}"


def get_flag_tail(tail_length):
    ps.sendlineafter(b"Choice? ", str(2).encode())
    ps.sendlineafter(b"Length? ", str(tail_length).encode())
    line = ps.recvline().strip()
    b64_encrypted_tail = line.split(b"Result: ")[-1]

    return b64_encrypted_tail

# Brute-force the flag character by character from the end
# by gradually building a flag fragment, incrementing the length as we discover new characters.
def brute_force__flag(temp_flag):
    for tail_length in range(2, 100):
        b64_flag_tail = get_flag_tail(tail_length)

        # Loop through ASCII printable chars.
        for ascii_value in range(32, 127):
            # Choose the option "Encrypt chosen plaintext".
            ps.sendlineafter(b"Choice? ", str(1).encode())
            # Encrypt the flag + current guessed character.
            fragment = chr(ascii_value) + temp_flag
            ps.sendlineafter(b"Data? ", fragment.encode())

            # Receive the encrypted fragment of the guessed flag.
            line = ps.recvline().strip()
            b64_encrypted_fragment = line.split(b"Result: ")[-1]

            # Compare flag fragment to flag tail.
            if b64_encrypted_fragment == b64_flag_tail:
                # Append the correct character to the flag.
                print(f"Found character: {chr(ascii_value)}")
                temp_flag = chr(ascii_value) + temp_flag
                break

        if "KEY_WORD" in temp_flag:
            return temp_flag
                
def main():
    flag = brute_force__flag(temp_flag)
    print(f"\n{GREEN}{flag}{RESET}\n")

if __name__ == "__main__":
    main()
