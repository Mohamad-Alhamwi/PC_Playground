from pwn import *

context(arch="amd64", os="linux", log_level="info")

challenge_path = "CHALLENGE_PROCESS"
ps = process(challenge_path)
key = ""
ciphertext = ""
plaintext = ""

while True:
    line = ps.recvline().strip()

    if b"The key: " in line:
        key = line.split(b"The key: ")[-1].decode()
        print(f"Key: {key}")

    if b"Encrypted secret: " in line:
        ciphertext = line.split(b"Encrypted secret: ")[-1].decode()
        print(f"Key: {ciphertext}")
        break

plaintext_int = int(key) ^ int(ciphertext)
print(f"Plaintext: {plaintext_int}")
        
ps.sendlineafter(b"Decrypted secret? ", str(plaintext_int).encode())

ps.interactive()
