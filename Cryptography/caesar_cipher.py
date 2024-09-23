def shift(shift_amount, plaintext):
    ciphertext = ""

    for char in plaintext:
        temp_int = ord(char) + shift_amount
        temp_char = chr(temp_int)
        ciphertext  += temp_char

    return ciphertext

def deshift(shift_amount, ciphertext):
    plaintext = ""

    for char in ciphertext:
        temp_int = ord(char) - shift_amount
        temp_char = chr(temp_int)
        plaintext  += temp_char

    return plaintext

def main():
    ciphertext = "fdhvduflskhu"
    plaintext = ""
    shift_amount = 3

    plaintext = deshift(shift_amount, ciphertext)
    print(f"Plaintext is: {plaintext}")

    ciphertext = shift(shift_amount, plaintext)
    print(f"Ciphertext is: {ciphertext}")

if __name__ == "__main__":
    main()
