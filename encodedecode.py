import arithmetic_logic_unit

XLEN = 32

HEX_DIGITS = ['0', '1', '2', '3', '4', '5', '6', '7',
              '8', '9', 'A', 'B', 'C', 'D', 'E', 'F']

def int_to_bitvector(value):
    bits = [0]*XLEN
    is_negative = value < 0
    abs_val = value
    if is_negative:
        abs_val = -value  # in tests only; later implement manually with subtraction

    # Compute bits manually from MSB to LSB
    for i in range(XLEN-1, -1, -1):
        power_of_2 = 1
        for _ in range(XLEN-1-i):
            power_of_2 += power_of_2  # double without *
        if abs_val >= power_of_2:
            abs_val -= power_of_2
            bits[i] = 1
    if is_negative:
        bits = twos_complement(bits)
    return bits

def bitvector_to_bin(bits): #convert to binary
    s = ''
    for b in bits:
        s += '1' if b else '0'
    return s

def bitvector_to_hex(bits): #convert to hex
    hex_str = ''
    for i in range(0, XLEN, 4):
        nibble = bits[i:i+4]
        # convert 4-bit nibble to decimal manually
        val = 0
        for j in range(4):
            if nibble[j]:
                power = 1
                for _ in range(3-j):
                    power += power  # double without *
                val += power
        hex_str += HEX_DIGITS[val]
    return hex_str


def encode_twos_complement(value):
    overflow_flag = False
    # Step 1: Detect overflow (outside -2**31..2**31-1)
    # Compare MSB + remaining bits (manual)
    if value < -(1 << (XLEN-1)) or value > ((1 << (XLEN-1)) - 1):
        overflow_flag = True

    bits = int_to_bitvector(value)
    bin_str = bitvector_to_bin(bits)
    hex_str = bitvector_to_hex(bits)
    return {'bin': bin_str, 'hex': hex_str, 'overflow_flag': overflow_flag}