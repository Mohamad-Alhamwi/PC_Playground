import base64

def one_time_pad(ciphertext, key):
    # Decode the ciphertext and key from Base64
    decoded_ciphertext = base64.b64decode(ciphertext)
    decoded_key = base64.b64decode(key)

    # Ensure the key is at least as long as the ciphertext for perfect secrecy.
    if len(decoded_key) < len(decoded_ciphertext):
        raise ValueError("Key must be at least as long as the ciphertext.")

    # XOR the ciphertext with the key
    flag_bytes = bytes(a ^ b for a, b in zip(decoded_ciphertext, decoded_key))

    # Convert the result to a string.
    flag = flag_bytes.decode('utf-8', errors='ignore')

    return flag

def main():
    key = "sYkGlT1HsC76hhEYbQFd3P3Y44Pm863er8dmpKeAyIGjBTW5wpNMyH56yLIVtRoZJ3Nu2GjAvmWERg=="
    ciphertext = "wf5ou14o3EKf4XRjPEwkj8SBktuqxcKkxYJSze+yhPbRQ0DR9/Uv5hoosvxv+F5VFCIqlV2RxDL5TA=="
    
    flag = one_time_pad(ciphertext, key)

    print(f'Your flag is: {flag}')

if __name__ == "__main__":
    main()
