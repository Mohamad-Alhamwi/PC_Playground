##################################
########################### Steps:
# Input of 18 bytes length.
# XoR'ed with 0x6c.
# Reversed
##################################

def reverse(given_output):
    # Initialize a list of length 18 with zeros.
    original_input = [0] * 18

    # Unreverse the elements.
    given_output.reverse()

    # Unxor the elements.
    for counter in range(18):
        original_input[counter] = hex(given_output[counter] ^  0x6c)

    return original_input

def main():
    # Given sorted output
    given_output = [0x02, 0x05, 0x06, 0x07, 0x07, 0x08, 0x0d, 0x0e, 0x14, 0x14, 0x16, 0x16, 0x16, 0x16, 0x19, 0x1b, 0x1d, 0x1d]

    original_input = reverse(given_output)

    # Create the echo command
    echo_command = 'echo -e "' + ''.join([f'\\x{hex_val[2:]}' for hex_val in original_input]) + '"'

    print(echo_command)

if __name__ == "__main__":
    main()
