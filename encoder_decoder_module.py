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
    bits = bits[-XLEN:]
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

    if neg:
        result = -result

    return result

# WHAT IS THIS????????????????????????
def init_bitvector_from_int(value, length=8):
    bits = []
    for i in reversed(range(length)):
        # Check if the current bit is 1
        if value & (1 << i):
            bits.append(1)
        else:
            bits.append(0)
    return bits

def init_bitvector_from_int_no_mask(value, length=8):
    bits = [0] * length

    # Step 1: Build a bitvector representing the value using repeated increment
    value_bits = [0] * length
    one = [0]*(length-1) + [1]
    for _ in range(value):
        value_bits, _ = alu.ADD(value_bits, one)

    # Step 2: Extract each bit from MSB to LSB
    for i in range(length):
        # Create a bitvector representing the current power of two
        power_bits = [0]*i + [1] + [0]*(length-i-1)

        # If remaining value_bits >= power_bits, set bit 1 and subtract
        if alu.compare_bitvectors_gt(value_bits, power_bits) or value_bits == power_bits:
            bits[i] = 1
            value_bits, _ = alu.SUB(value_bits, power_bits)
        else:
            bits[i] = 0

    return bits

def init_bitvector_from_int(value, length=8):
    # Step 1: Initialize output bitvector
    bits = [0] * length

    # Step 2: Convert value into bitvector directly using operators
    # (This replaces the repeated ADD loop)
    value_bits = [(value >> (length - 1 - i)) & 1 for i in range(length)]

    # Step 3: Extract each bit from MSB to LSB using bitvector operations
    one = [0] * (length - 1) + [1]  # single-bit vector
    remaining_bits = value_bits[:]   # copy for manipulation

    for i in range(length):
        # Create power-of-two bitvector at current position
        power_bits = alu.SLL(one, length - 1 - i)

        # If remaining_bits >= power_bits, set bit 1 and subtract
        if alu.compare_bitvectors_gt(remaining_bits, power_bits) or remaining_bits == power_bits:
            bits[i] = 1
            remaining_bits, _ = alu.SUB(remaining_bits, power_bits)
        else:
            bits[i] = 0

    return bits
