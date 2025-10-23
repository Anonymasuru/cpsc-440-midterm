import arithmetic_logic_unit as alu
XLEN = 32

def encoded_twos_complement(value: int):
    bits = [0,0] + alu.init_bitvector()

    # Step 1: Handle sign and absolute value
    neg = value < 0
    value_abs = -value if neg else value

    # Step 2: Convert magnitude to binary using a for loop
    # We'll iterate once per bit position (starting from LSB)
    temp_val = value_abs
    for i in range(len(bits)):  # avoid using XLEN + EXT directly
        remainder = temp_val % 2     # extract current bit
        temp_val = temp_val // 2     # shift right logically
        bits[-1 - i] = remainder     # fill from LSB toward MSB

    # Step 3: Apply two’s complement if number was negative
    if neg:
        bits = alu.twos_complement(bits)

    # Step 4: Overflow detection using sign-extension mismatch
    # If all extra MSBs equal to sign bit, no overflow.
    sign_bit = bits[2]  # the original MSB
    overflow = 0
    for i in range(2):  # the extra MSBs
        if bits[i] != sign_bit:
            overflow = 1
            break

    # Step 5: Trim down to XLEN bits
    bits = bits[-XLEN:]

    # Step 5: Convert to hex using 4-bit lookup table
    nibble_to_hex = {
        (0,0,0,0): '0', (0,0,0,1): '1', (0,0,1,0): '2', (0,0,1,1): '3',
        (0,1,0,0): '4', (0,1,0,1): '5', (0,1,1,0): '6', (0,1,1,1): '7',
        (1,0,0,0): '8', (1,0,0,1): '9', (1,0,1,0): 'A', (1,0,1,1): 'B',
        (1,1,0,0): 'C', (1,1,0,1): 'D', (1,1,1,0): 'E', (1,1,1,1): 'F'
    }
    hex_str = ''
    for i in range(0, XLEN, 4):
        nibble = tuple(bits[i:i+4])
        hex_str += nibble_to_hex[nibble]

    return {
        "bin": alu.bits_to_str(bits),
        "hex": hex_str,
        "overflow": overflow
    }

def decoded_twos_complement(value):
    # Step 1: Detect and normalize input
    # If it's a string, convert to bit list
    if isinstance(value, str):
        bits = alu.str_to_bits(value)
    else:
        bits = value[:]  # assume already list of bits, copy for safety

    # Step 2: Interpret sign bit
    neg = bits[0] == 1

    # Step 3: If negative, convert from two’s complement to magnitude
    if neg:
        mag_bits = alu.twos_complement(bits)
    else:
        mag_bits = bits

    # Step 4: Convert bitvector to integer
    result = 0
    for bit in mag_bits:
        result = (result * 2) + bit

    # Step 5: Reapply sign
    if neg:
        result = -result

    return result