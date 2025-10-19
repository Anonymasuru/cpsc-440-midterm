XLEN = 32



def encoded_twos_complement(value: int):
    max = 2**(XLEN - 1) - 1 # Highest numeric limit. one must be rmeoved because its the sign indicator (leading zero)
    min = -2**(XLEN - 1) # Lowest numberic limit. not required because the negative sign indicator itself is a viable value
    overflow_flag = not (min <= value <= max) # Overflow check. Value must be within min and max.
    if value < 0: # If negative
        value = (1 << XLEN) + value # wrap around and replace the number with the two's complement integer value
    bin = format(value, f'0{XLEN}b') # integer in binaric. Pad zeroes to match XLEN.
    hex = format(value,f'#0{XLEN // 4}X') # integer in hex.
    return {
        "binary": bin,
        "hex": hex,
        "overflow": overflow_flag
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