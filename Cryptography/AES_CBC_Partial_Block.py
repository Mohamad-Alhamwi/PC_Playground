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
    iv, ciphertext = data[:16], data[16:]

    tampered_iv = bytearray(b"\x00" * 16)
    intermediate_block = [0] * 16
    ps_worker.recv()
    index = 15
    byte = 0
    padding = 1
    print('\n')

    while index >= 0:

        temp = padding - 1

        while byte <= 255:

            while temp > 0:

                tampered_iv[index + temp] = intermediate_block[index + temp] ^ padding
                temp -= 1
            
            tampered_iv[index] = byte
            tampered_data = b"TASK: " + (tampered_iv + ciphertext).hex().encode()
            ps_worker.sendline(tampered_data)
            worker_result = ps_worker.recv()

            #print(f"{RED}{byte}{RESET}-----{GREEN}{worker_result.decode()}{RESET}")
            if b"Unknown command!" in worker_result:
                print(f"Got a hit! {RED}{byte}{RESET}")
                intermediate_block[index] = byte ^ padding
                padding = padding + 1
                byte = 0
                break
            
            byte = byte + 1

        index = index - 1
        byte = 0

    recovered_pw = strxor(bytes(intermediate_block), iv)
    recovered_pw = unpad(recovered_pw, 16)
    ps_redeem = process("CHALLENGE_FILE")
    ps_redeem.sendlineafter(b"Password?", recovered_pw)
    print(ps_redeem.recvall().decode().strip())

if __name__ == "__main__":
    main()
