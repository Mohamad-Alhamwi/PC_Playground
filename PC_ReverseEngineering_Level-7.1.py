#################################################
########################################## Steps:
# 28 Input => Sort => swap => XOR => swap => XOR.
#################################################

def unswap(expected_key):
    # swap the elements.
    for index in range(14):
        expected_key[index], expected_key[27 - index] = expected_key[27 - index], expected_key[index]

def unxor(expected_key, key1, key2, key3):
    for index in range(28):
        remainder = index % 3

        if remainder == 2: 
            expected_key[index] = expected_key[index] ^ key1

        elif remainder < 3:
            if remainder == 0:
                expected_key[index] = expected_key[index] ^ key2
                
            elif remainder == 1: 
                expected_key[index] = expected_key[index] ^ key3

def reverse(expected_key):
    # Unxor the elements.
    unxor(expected_key, 0x93, 0x90, 0x78)

    # Unswap the elements.
    unswap(expected_key)

    # Unxor the elements.
    unxor(expected_key, 0x35, 0xe4, 0x2b)
    
    # Unswap the elements.
    unswap(expected_key)

    return expected_key

def main():
    # expected key in hexadecimal values (stored as integers).
    expected_key = [0x16, 0x29, 0xDD, 0x11, 0x25, 0xD0, 0x1D, 0x27, 0xD2, 0x1F, 0x20, 0xD6, 0x1A, 0x23, 0xD7, 0x07, 0x3E, 0xCB, 0x01, 0x3B, 0xCF, 0x0C, 0x35, 0xC0, 0x0D, 0x34, 0xC2, 0x0E]

    original_key = reverse(expected_key)

    original_hex_key = [hex(element) for element in original_key]

    # Create the echo command
    echo_command = 'echo -e "' + ''.join([f'\\x{hex_value[2:]}' for hex_value in original_hex_key]) + '"'

    print(echo_command)

if __name__ == "__main__":
    main()
