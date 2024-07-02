import base64
from Crypto.Cipher import AES

def unpad(padded_value):
    # Get the value of the last byte.
    pad_length = padded_value[-1]

    # Remove the last 'pad_len' bytes.
    original_value = padded_value[:-pad_length]
    return original_value

def AES_ECB(secret_ciphertext, key):
    # Decode.
    de_secret_ciphertext = base64.b64decode(secret_ciphertext)
    de_key = base64.b64decode(key)

    # Create AES cipher in ECB mode. 
    cipher = AES.new(key=de_key, mode=AES.MODE_ECB)

    # Decrypt the ciphertext.
    decrypted_bytes = cipher.decrypt(de_secret_ciphertext)

    # Unpad the decrypted bytes.
    flag_bytes = unpad(decrypted_bytes)

    flag = flag_bytes.decode('utf-8', errors='ignore')

    return flag

def main():
    key = "CQCVbJdSAhpZwMWz6ENkGQ=="
    secret_ciphertext = "5sExfqkh5PcGUDrjQ4T1HzZ39mMCsEUpobc/Xb+EomogoiPOmRKcTKo0xX4nmV/0LsUodTJO/gjl5gSXX1x6vA=="

    flag = AES_ECB(secret_ciphertext, key)

    print(f'Your flag is: {flag}')

if __name__ == "__main__":
    main()
