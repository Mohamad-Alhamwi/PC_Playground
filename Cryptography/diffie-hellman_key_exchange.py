#!/bin/python3

from pwn import *
import random
from Crypto.Util.strxor import strxor

context.arch = 'amd64'

ps = process("/CHALLENGE_FILE")

# Agreed upon, publicly known value.
p = int.from_bytes(bytes.fromhex(
    "FFFFFFFF FFFFFFFF C90FDAA2 2168C234 C4C6628B 80DC1CD1 "
    "29024E08 8A67CC74 020BBEA6 3B139B22 514A0879 8E3404DD "
    "EF9519B3 CD3A431B 302B0A6D F25F1437 4FE1356D 6D51C245 "
    "E485B576 625E7EC6 F44C42E9 A637ED6B 0BFF5CB6 F406B7ED "
    "EE386BFB 5A899FA5 AE9F2411 7C4B1FE6 49286651 ECE45B3D "
    "C2007CB8 A163BF05 98DA4836 1C55D39A 69163FA8 FD24CF5F "
    "83655D23 DCA3AD96 1C62F356 208552BB 9ED52907 7096966D "
    "670C354E 4ABC9804 F1746C08 CA18217C 32905E46 2E36CE3B "
    "E39E772C 180E8603 9B2783A2 EC07A28F B5C55DF0 6F4C52C9 "
    "DE2BCBF6 95581718 3995497C EA956AE5 15D22618 98FA0510 "
    "15728E5A 8AACAA68 FFFFFFFF FFFFFFFF"
), "big")

# Agreed upon, publicly known value.
g = 2

# Bob's private kay.
b = random.getrandbits(2048)

# Bob computes and sends alice his public key.
B = pow(g, b, p)
B = hex(B)

# Get Alice's public key.
while True:
    A = ps.recvline().strip()
    
    if not b"A: " in A:
        continue
    else:
        A = A.split(b"A: ")[-1]
        A = A.decode()
    
        A = int(A, 16)
        break

# Compute the shared key.
s = pow(A, b, p)
key = s.to_bytes(256, "little")

ps.sendlineafter(b"B: ", str(B).encode())

# Get the secret ciphertext.
ciphertext = ps.recvline().strip()
ciphertext = ciphertext.split(b"secret ciphertext (b64): ")[-1]
ciphertext = ciphertext.decode()
ciphertext = base64.b64decode(ciphertext)

# Extract the flag.
flag = strxor(ciphertext , key[:len(ciphertext)])
flag = flag.decode("utf-8").strip()
print(repr(f"Flag: {flag}"))
