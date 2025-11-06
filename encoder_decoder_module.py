import arithmetic_logic_unit as alu
XLEN = 32

# This is usually part of the register file write logic or instruction execution stage, not the ALU itself.

def encoded_twos_complement(value: int):
    # overflow check
    overflow = value < -(2 ** (XLEN - 1)) or value > (2 ** (XLEN - 1)) - 1
    # negative check
    neg = value < 0
    magnitude = -value if neg else value

    # convert mag to bitvector
    bits = []
    for i in reversed(range(XLEN)):
        bits.append(1 if magnitude & (1 << i) else 0)
    if neg:
        bits = alu.twos_complement(bits)
    # binary output
    bin_str = alu.bits_to_str(bits)
    # hex output
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
        "bin": bin_str,
        "hex": hex_str,
        "overflow": overflow
    }


def decoded_twos_complement(value):
    # if string, convert to bitvector
    if isinstance(value, str):
        bits = alu.str_to_bits(value)
    else:
        bits = value[:] # copying list
    # negative check
    neg = bits[0] == 1
    if neg:
        mag_bits = alu.twos_complement(bits)
    else:
        mag_bits = bits
    # convert bitvector to integer
    result = 0
    for bit in mag_bits:
        result = (result * 2) + bit
    if neg:
        result = -result
    return result

def sign_extend(bits, target_length):
    current_len = len(bits)
    # check if already at or above target length
    if current_len >= target_length:
        return bits[-target_length:]
    msb = bits[0] 
    extension = [msb] * (target_length - current_len)
    return extension + bits


def zero_extend(bits, target_length):
    current_len = len(bits)
    # check if already at or above target length
    if current_len >= target_length:
        return bits[-target_length:]
    extension = [0] * (target_length - current_len)
    return extension + bits
