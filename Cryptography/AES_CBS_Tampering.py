#!/bin/python3

from pwn import *
from Crypto.Util.Padding import pad
from Crypto.Util.strxor import strxor
context.arch = 'amd64'

#challenge_file = "CHALLENGE_FILE"
#ps = process(challenge_file)
ps_dispatcher = process("CHALLENGE_FILE")
ps_worker = process("CHALLENGE_FILE")
GREEN = "\033[92m"
RED = "\033[95m"
RESET = "\033[0m"

def main():    
    line = ps_dispatcher.recvline()
    hex_ciphertext = line.split(b'TASK: ')[-1].decode().strip()
    cipher_block = bytes.fromhex(hex_ciphertext)
    iv, ciphertext = cipher_block[:16], cipher_block[16:]
    plaintext = "sleep"

    ## C0 = AES_ENCRYPT(IV ^ P1).
    ## P1 = AES_DECRYPT(C0) ^ IV.
    ## IV = P1 ^ AES_DECRYPT(C0).
    ## "flag!" = AES_DECRYPT(C0) ^ IV.
    ## TAMPARED_IV = AES_DECRYPT(AES_ENCRYPT(IV ^ P1)) ^ "flag!".
    ## TAMPARED_IV = IV ^ P1 ^ "flag!".
    ## TAMPARED_IV = IV ^ "sleep" ^ "flag!".

    temp = strxor(pad(b"sleep", 16), pad(b"flag!", 16))
    tampered_iv = strxor(iv , temp)
    tampered_ciphertext = b"TASK: " + (tampered_iv + ciphertext).hex().encode()

    ps_worker.sendline(tampered_ciphertext)
    while True:
        worker_result = ps_worker.recv()
        
        if b"Victory! Your flag:" in worker_result:
            continue
        break
    
    print(f"\n{GREEN}{worker_result.decode()}{RESET}")

if __name__ == "__main__":
    main()
