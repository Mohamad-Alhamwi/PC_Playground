from pwn import *
import json
from hashlib import sha256
from Crypto.PublicKey import RSA

context(arch="amd64", os="linux", log_level="info")

modulus_n = ""
private_key_d = ""
public_key_e = ""
root_certificate_json = ""

challenge_path = "CHALLENGE_FILE"
ps = process(challenge_path)

while True:
    line = ps.recvline()

    if b"root key d: " in line:
        hex_root_private_key = line.split(b"root key d: ")[-1].decode()
        private_key_d = int(hex_root_private_key, 16)
    elif b"root certificate (b64): " in line:
        root_certificate = base64.b64decode(line.split(b"root certificate (b64): ")[-1].decode())
        root_certificate_json = json.loads(root_certificate)
        modulus_n = root_certificate_json["key"]["n"]
        public_key_e = root_certificate_json["key"]["e"]
    elif b"root certificate signature (b64): " in line:
        b64_root_certificate_signature = line.split(b"root certificate signature (b64): ")[-1].decode()
        break

## Hash root certificate.
hashed_certificate = sha256(root_certificate).digest()
hashed_int = int.from_bytes(hashed_certificate, byteorder='little')

## Sign root certificate.
signed_certificate = pow(hashed_int, private_key_d, modulus_n)
signed_certificate_bytes = signed_certificate.to_bytes(256, byteorder='little')

print(f"\nSigned Certificate: {base64.b64encode(signed_certificate_bytes).decode()}")
print(f"\nRoot Certificate Signature (b64): {b64_root_certificate_signature}")

user_key = RSA.generate(1024)

user_certificate = {
    "name": "user",
    "key": {
        "e": user_key.e,
        "n": user_key.n,
    },
    "signer": "root",
}

## Hash user certificate.
hashed_user_certificate = sha256(json.dumps(user_certificate).encode("ascii")).digest()
hashed_user_certificate_int = int.from_bytes(hashed_user_certificate, byteorder='little')

## Sign user certificate.
signed_user_certificate = pow(hashed_user_certificate_int, private_key_d, modulus_n)
signed_user_certificate_bytes = signed_user_certificate.to_bytes(256, byteorder='little')

ps.sendlineafter(b"user certificate (b64): ", base64.b64encode(json.dumps(user_certificate).encode("ascii")))
ps.sendlineafter(b"user certificate signature (b64):", base64.b64encode(signed_user_certificate_bytes))

line = ps.recvline()
secret_ciphertext_b64 = line.split(b"secret ciphertext (b64): ")[-1]
secret_ciphertext_bytes = base64.b64decode(secret_ciphertext_b64)
secret_ciphertext_int = int.from_bytes(secret_ciphertext_bytes, byteorder='little')
secret_ciphertext = pow(secret_ciphertext_int, user_key.d, user_key.n).to_bytes(256, byteorder='little').rstrip(b'\0')
print(f"Flag: {secret_ciphertext.decode()}")

ps.interactive()


