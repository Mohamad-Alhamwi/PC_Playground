#!/bin/python3

from pwn import *
from Crypto.Util.Padding import pad, unpad
from Crypto.Util.strxor import strxor
context.arch = 'amd64'

ps_dispatcher = process("CHALLENGE_FILE")
ps_worker = process("CHALLENGE_FILE")
GREEN = "\033[92m"
RED = "\033[95m"
RESET = "\033[0m"

def main():    
    line = ps_dispatcher.recvline()
    hex_ciphertext = line.split(b'TASK: ')[-1].decode().strip()
    data = bytes.fromhex(hex_ciphertext)

    tampered_ciphertext = bytearray(b"\x00" * 16)
    byte = 0
    print('\n')

    block_count = (len(data) - 16) // 16                # excludes IV.
    for block_index in range(block_count - 1, -1, -1):  # 3 down to 0
        start = 16 + block_index * 16                   # skip IV at offset 0
        ciphertext_block = data[start : start + 16]
        previous_ciphertext_block = data[start - 16 : start]
        intermediate_block = [0] * 16
        index = 15
        padding = 1

        while index >= 0:
            temp = padding - 1

            while byte <= 255:

                while temp > 0:

                    tampered_ciphertext[index + temp] = intermediate_block[index + temp] ^ padding
                    temp -= 1
                
                tampered_ciphertext[index] = byte
                tampered_data = b"TASK: " + (tampered_ciphertext + ciphertext_block).hex().encode()
                ps_worker.sendline(tampered_data)
                worker_result = ps_worker.recv()

                if b"Unknown command!" in worker_result:
                    print(f"Got a hit! {RED}{byte}{RESET}")
                    intermediate_block[index] = byte ^ padding
                    padding = padding + 1
                    byte = 0
                    break
                
                byte = byte + 1

            index = index - 1
            byte = 0

        print("Recovering the flag ...")
        recovered_flag = strxor(bytes(intermediate_block), previous_ciphertext_block)
        print(f"Block #{block_index}: {recovered_flag}\n")

if __name__ == "__main__":
    main()
