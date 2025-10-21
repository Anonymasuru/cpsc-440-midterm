# We're going to need to build this from the ground up.
XLEN = 32
# These operators appear to go through the entire array and produce results based on their logic criteria

# if both inputs are on
def AND(a, b): 
    if a == 1 and b == 1:
        return 1
    else:
        return 0

# if one input is on
def OR(a, b): 
    if a == 1 or b == 1:
        return 1
    else:
        return 0

# if inputs are different
def XOR(a, b): 
    if a != b:
        return 1
    else:
        return 0

# essentially flips the bit
def NOT(a):
    if a == 0:
        return 1
    else:
        return 0

def twos_complement(a):
    inverted = []
    for bit in a:
        inverted.append(NOT(bit))
    one = init_bitvector()
    one[-1] = 1
    result, _ = ADD(inverted, one)
    return result

def bits_to_str(bits):
    return ''.join(str(b) for b in bits)

#========
#SHIFTERS
#========

def SLL(rs1, n):
    # Copy the input to avoid modifying it directly
    shifted = rs1[:]

    # Perform the shift 'n' times
    for _ in range(n):
        shifted.pop(0)      # Remove the most significant bit (MSB)
        shifted.append(0)   # Add a zero at the least significant bit (LSB)
    
    return shifted

def SRL(rs1, n):
    shifted = rs1[:]  # copy to avoid mutating original

    for _ in range(n):
        shifted.pop()       # remove the rightmost bit (LSB)
        shifted.insert(0, 0)  # insert 0 at the left (MSB)

    return shifted

def SRA(rs1, n):
    shifted = rs1[:]  # copy to avoid mutating original
    msb = rs1[0]      # store the original sign bit

    for _ in range(n):
        shifted.pop()         # remove LSB
        shifted.insert(0, msb)  # insert MSB (sign bit) at left

    return shifted

def init_bitvector():
    bitvector = [0 for _ in range(XLEN)] 
    return bitvector

#======
#ADDERS
#======

def half_adder(a, b):
    # sum is 1 if exactly one of a, b is 1 (THIS IS XOR)
    sum_bit = XOR(a, b)
    # carry is 1 only if both a and b are 1 (THIS IS AND)
    carry = AND(a, b)
    return sum_bit, carry

def full_adder(a, b, carry_in):
    # first half adder
    sum1, carry1 = half_adder(a, b)
    # second half adder with carry_in
    sum2, carry2 = half_adder(sum1, carry_in)
    carry_out = OR(carry1, carry2)
    return sum2, carry_out

#==============
#BITVECTOR MATH
#==============

def ADD(rs1, rs2):
    result = init_bitvector()
    carry = 0
    for i in range(31, -1, -1): # In the event we ever switch off of 32bit, this needs to be adjusted.
        sum_bit, carry = full_adder(rs1[i], rs2[i], carry)
        result[i] = sum_bit
    # Flag checks
    N = result[0]                                                 # Negative flag
    Z = 1                                                         # Zero flag
    for bit in result:
        Z = AND(Z, XOR(bit, 1))               
    C = carry                                                     # Carry out of MSB
    V = AND(NOT(XOR(rs1[0], rs2[0])), XOR(result[0], rs1[0]))     # Overflow flag
    return result[-XLEN:], {"N": N, "Z": Z, "C": C, "V": V}

def SUB(rs1, rs2):
    neg_rs2 = twos_complement(rs2)
    result, flags = ADD(rs1, neg_rs2)
    flags['C'] = XOR(flags['C'], 1)
    flags['V'] = AND(XOR(rs1[0], rs2[0]), XOR(result[0], rs1[0]))
    return result[-XLEN:], flags

#===========
#MULTIPLIERS
#===========

def MUL(rs1, rs2):
    accumulator = init_bitvector()
    multiplicand = rs1[:]
    multiplier = rs2[:]
    overflow = 0 
    step = 0 # MUL tracing requirement

    for _ in range(XLEN):
        if multiplier[-1] == 1:
            print("  -> LSB = 1, adding multiplicand to accumulator")
            accumulator, flags = ADD(accumulator, multiplicand)
            if flags["C"] == 1:   # carry-out from ADD MSB
                overflow = 1
        else:
            print("  -> LSB = 0, skipping addition")

        # Before shifting multiplicand, check if MSB will be lost
        if multiplicand[0] == 1:
            overflow = 1

        multiplicand = SLL(multiplicand, 1)
        multiplier = SRL(multiplier, 1)

        #trace code here
        print("Step:", step)
        print("  Accumulator:", bits_to_str(accumulator))
        print("  Multiplier: ", bits_to_str(multiplier))
        print("  Multiplicand:", bits_to_str(multiplicand))

        step = step + 1 # illegal but strictly for tracing, not necessary otherwise

    return accumulator[-XLEN:], {"overflow": overflow}

def DIV(rs1, rs2):
    # Signed 32-bit division: returns quotient.
    # Can't divide by 0, return -1
    if rs2 == [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]:
        return [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
    neg_dividend = 1 if rs1[0] == 1 else 0
    neg_divisor = 1 if rs2[0] == 1 else 0
    # Step 2: Take absolute values
    dividend = twos_complement(rs1) if neg_dividend else rs1[:]
    divisor = twos_complement(rs2) if neg_divisor else rs2[:]
    # init quotient and remainder
    quotient = init_bitvector()
    remainder = init_bitvector()
    for i in range(XLEN):
        # Shift remainder left, bring in next dividend bit
        remainder = SLL(remainder, 1)
        remainder[-1] = dividend[i]
        # Compare remainder >= divisor
        if remainder >= divisor:
            remainder, _ = SUB(remainder, divisor)
            quotient[i] = 1

    # Step 4: Apply quotient sign
    if XOR(neg_dividend,neg_divisor) == 1:
        quotient = twos_complement(quotient)

    # Step 5: Apply remainder sign (same as dividend)
    if neg_dividend:
        remainder = twos_complement(remainder)

    return quotient