from pwn import *

context(arch="amd64", os="linux", log_level="info")

challenge_path = "CHALLENGE_FILE_1"

flag_bytes = "flag".encode("ascii")
flag_int = int.from_bytes(flag_bytes, "little")

print(flag_int)

###########
#flag:1734437990 = 2 · 5 · 19 · 1033 · 8837

f1_int =  2
f2_int =  5
f3_int = 19
f4_int = 1033
f5_int = 8837

f1_bytes = f1_int.to_bytes(1, "little")
f2_bytes = f2_int.to_bytes(1, "little")
f3_bytes = f3_int.to_bytes(1, "little")
f4_bytes = f4_int.to_bytes(2, "little")
f5_bytes = f5_int.to_bytes(2, "little")

f1_bytes_b64_encoded = base64.b64encode(f1_bytes)
f2_bytes_b64_encoded = base64.b64encode(f2_bytes)
f3_bytes_b64_encoded = base64.b64encode(f3_bytes)
f4_bytes_b64_encoded = base64.b64encode(f4_bytes)
f5_bytes_b64_encoded = base64.b64encode(f5_bytes)

to_be_signed_factors = [f1_bytes_b64_encoded, f2_bytes_b64_encoded, f3_bytes_b64_encoded, f4_bytes_b64_encoded, f5_bytes_b64_encoded]
signed_factors = []

for index in range (len(to_be_signed_factors)):
    ps = process([challenge_path, to_be_signed_factors[index]])

    # Receive flag from the process
    signed_factor = ps.recvline().decode().strip().split("Signed command (b64): ")[-1]
    signed_factors.append(signed_factor)
    ps.close()

for index in range (len(signed_factors)):
    print(signed_factors[index])
    print("\n")

## So far so good.

flag_int = 1 
for index in range (len(signed_factors)):
    flag_int *= int.from_bytes(base64.b64decode(signed_factors[index]), "little")
    print("\n")

flag_bytes = flag_int.to_bytes(2048, "little")
challenge_path = "CHALLENGE_FILE_2"
ps = process([challenge_path,  base64.b64encode(flag_bytes)])

ps.interactive()


