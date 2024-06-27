########################################################
################################################# Steps:
# 35 bytes => Reverse => XOR => Sort => XOR => XOR => XOR => Swap
########################################################

def unswap(expected_key, index1, index2):
    # Swap the elements.
    expected_key[index1], expected_key[index2] = expected_key[index2], expected_key[index1]

def unreverse(expected_key):
    expected_key_length = len(expected_key)

    # Reverse the elements.
    for index in range(expected_key_length // 2):
        expected_key[index], expected_key[expected_key_length - 1 - index] = expected_key[expected_key_length - 1 - index], expected_key[index]

def unxor(expected_key, key):
    expected_key_length = len(expected_key)

    # Convert the key to an array of bytes
    key_bytes = key.to_bytes((key.bit_length() + 7) // 8, 'big')
    key_length = len(key_bytes)

    # XOR each element of expected_key with the corresponding byte from key_bytes
    for index in range(expected_key_length):
        expected_key[index] = expected_key[index] ^ key_bytes[index % key_length]

def reverse(expected_key):
    # Unswap the elements.
    unswap(expected_key, 11, 32)

    # Unxor the elements.
    unxor(expected_key, 0x66bb4f3a52c281)
    unxor(expected_key, 0xd0d13d914fc2cd)
    unxor(expected_key, 0x83c9c105)
    unxor(expected_key, 0xb2)

    # Unreverse the elements.
    unreverse(expected_key)

    return expected_key

def main():
    # expected key in hexadecimal values (stored as integers).
    expected_key = [0xf5, 0x61, 0x70, 0x6d, 0x5a, 0x0c, 0x4b, 0x75, 0x2f, 0x7c, 0xad, 0x40, 0x44, 0x4d, 0xbc, 0xbf, 0x22, 0xb6, 0x09, 0xd3, 0x17, 0xa7, 0x71, 0xad, 0xf3, 0x0f, 0x1a, 0x95, 0xe9, 0x7e, 0x6d, 0x70, 0xdf, 0x16, 0x52]
    
    original_key = reverse(expected_key)

    original_hex_key = [hex(element) for element in original_key]

    # Create the echo command
    echo_command = 'echo -e "' + ''.join([f'\\x{hex_value[2:]}' for hex_value in original_hex_key]) + '"'

    print(echo_command)

if __name__ == "__main__":
    main()

