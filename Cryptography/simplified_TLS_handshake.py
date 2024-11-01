from pwn import *
import json
from hashlib import sha256
from Crypto.PublicKey import RSA
from Crypto.Random.random import getrandbits
from Crypto.Hash.SHA256 import SHA256Hash
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

context(arch="amd64", os="linux", log_level="info")
dhke_modules = ""
dhke_base = ""
dhke_client_public_key = ""
dhke_server_private_key = getrandbits(2048)
CA_modulus = ""
CA_private_key = ""
CA_public_key = ""
CA_certificate_json = ""
b64_CA__certificate_signature = ""
user_name = ""


challenge_path = "CHALLENGE_PATH"
ps = process(challenge_path)

while True:
    line = ps.recvline()

    if b"p: " in line:
        hex_dhke_modules = line.split(b"p: ")[-1].decode()
        dhke_modules = int(hex_dhke_modules, 16)
    elif b"g: " in line:
        hex_dhke_base = line.split(b"g: ")[-1].decode()
        dhke_base = int(hex_dhke_base, 16)
    elif b"root key d: " in line:
        hex_CA_private_key = line.split(b"root key d: ")[-1].decode()
        CA_private_key = int(hex_CA_private_key, 16)
    elif b"root certificate (b64): " in line:
        CA_certificate = base64.b64decode(line.split(b"root certificate (b64): ")[-1].decode())
        CA_certificate_json = json.loads(CA_certificate)
        CA_modulus = CA_certificate_json["key"]["n"]
        CA_public_key = CA_certificate_json["key"]["e"]
    elif b"root certificate signature (b64): " in line:
        b64_CA__certificate_signature = line.split(b"root certificate signature (b64): ")[-1].decode()
    elif b"name: " in line:
        user_name = line.split(b"name: ")[-1].decode().rstrip()
    elif b"A: " in line:
        hex_dhke_client_public_key = line.split(b"A: ")[-1].decode()
        dhke_client_public_key = int(hex_dhke_client_public_key, 16)
        break

## So far so good.

shared_secret = pow(dhke_client_public_key, dhke_server_private_key, dhke_modules)
key = SHA256Hash(shared_secret.to_bytes(256, "little")).digest()[:16]
cipher_encrypt = AES.new(key=key, mode=AES.MODE_CBC, iv=b"\0"*16)
cipher_decrypt = AES.new(key=key, mode=AES.MODE_CBC, iv=b"\0"*16)

dhke_server_public_key = pow(dhke_base, dhke_server_private_key, dhke_modules)
ps.sendlineafter(b"B: ",  hex(dhke_server_public_key).encode())

user_key = RSA.generate(1024)
user_public_key = user_key.e
user_private_key = user_key.d
user_modules = user_key.n

user_certificate = {
    "name": user_name,
    "key": {
        "e": user_public_key,
        "n": user_modules,
    },
    "signer": "root",
}

padded_data = pad(json.dumps(user_certificate).encode("ascii"), cipher_encrypt.block_size)
encrypted_data = cipher_encrypt.encrypt(padded_data)
ps.sendlineafter(b"user certificate (b64): ", base64.b64encode(encrypted_data))

## Hash user certificate.
hashed_user_certificate = sha256(json.dumps(user_certificate).encode("ascii")).digest()
hashed_user_certificate_int = int.from_bytes(hashed_user_certificate, byteorder='little')
## Sign user certificate.
signed_user_certificate = pow(hashed_user_certificate_int, CA_private_key, CA_modulus)
signed_user_certificate_bytes = signed_user_certificate.to_bytes(256, byteorder='little')
## Send user certificate
padded_data = pad(signed_user_certificate_bytes, cipher_encrypt.block_size)
encrypted_data = cipher_encrypt.encrypt(padded_data)
ps.sendlineafter(b"user certificate signature (b64): ", base64.b64encode(encrypted_data))

## Construct the data to be signed.
user_signature_data = (
    user_name.encode().ljust(256, b"\0") +
    dhke_client_public_key.to_bytes(256, "little") +
    dhke_server_public_key.to_bytes(256, "little")
)

## Sign the handshake.
user_signature_hash = SHA256Hash(user_signature_data).digest()
user_signature_int = int.from_bytes(user_signature_hash, byteorder="little")
user_signature = pow(user_signature_int, user_private_key, user_modules).to_bytes(256, "little")

## Send the signed user signature.
padded_signature = pad(user_signature, cipher_encrypt.block_size)
encrypted_signature = cipher_encrypt.encrypt(padded_signature)
ps.sendlineafter(b"user signature (b64): ", base64.b64encode(encrypted_signature))

## Get the flag.
line = ps.recvline()
encrypted_flag_b64 = line.split(b"secret ciphertext (b64): ")[-1]
encrypted_flag = base64.b64decode(encrypted_flag_b64)
flag = unpad(cipher_decrypt.decrypt(encrypted_flag), cipher_decrypt.block_size)
print(f"Flag: {flag.decode().rstrip()}")
ps.interactive()
