import arithmetic_logic_unit as alu
XLEN = 32

def DIV_two(vec):
    two_vec = alu.init_bitvector()
    two_vec[-1] = 1
    two_vec = alu.SLL(two_vec, 1)  # 0...010 = 2

    quotient, remainder = alu.DIV(vec, two_vec)  # existing ALU DIV
    return quotient, remainder


def encoded_twos_complement(value):
    XLEN = 32
    bits = [0] * XLEN  # Initialize 32-bit vector

    # Step 1: Handle sign and get absolute value
    negative = False
    if value < 0:
        negative = True
        value_abs = -value
    else:
        value_abs = value

    # Step 2: Convert magnitude to binary
    index = XLEN - 1  # Start filling from LSB
    while value_abs > 0 and index >= 0:
        bits[index] = value_abs % 2  # remainder is the current bit
        value_abs = value_abs // 2   # quotient for next iteration
        index -= 1

    # Step 3: Apply two's complement if original number was negative
    if negative:
        bits = alu.twos_complement(bits)

    # Step 4: Overflow detection
    max_vec = [0] + [1]*(XLEN-1)  # 0111...111
    min_vec = [1] + [0]*(XLEN-1)  # 1000...000
    overflow = 0
    if negative:
        for b_val, b_min in zip(bits, min_vec):
            if b_val > b_min:
                break
            elif b_val < b_min:
                overflow = 1
                break
    else:
        for b_val, b_max in zip(bits, max_vec):
            if b_val < b_max:
                break
            elif b_val > b_max:
                overflow = 1
                break

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
        "bin": alu.str_to_bits(bits),
        "hex": hex_str,
        "overflow": overflow
    }


print("Testing 'encoded_twos_complement' with 13 and -13...\n")
print(encoded_twos_complement(13))
print(encoded_twos_complement(-13))
print(encoded_twos_complement(2**31)) # Overflow test
def decoded_twos_complement(bits: str | int):
    #if isinstance(bits, int): # if bits is an int
    #    bits = format(bits & ((1 << XLEN) - 1), f'0{XLEN}b') # format to binary (still in integer?). Was bits = format(bits, f'0{XLEN}b')

    if not all(c in "01" for c in bits): # if string is not binary and not an int
        print("Input not a valid binary string or integer")
        return {"value": None} # return None
    value = int(bits, 2) # format in int
    if bits[0] == '1': # if MSB is 1 (negative binary)
        value -= (1 << XLEN) # wrap around
    return {"value": value}

print("\nTesting 'decoded_twos_complement'...\n")
print(decoded_twos_complement("00000000000000000000000000001101"))
print(decoded_twos_complement("11111111111111111111111111110011"))
print(decoded_twos_complement("LOL"))