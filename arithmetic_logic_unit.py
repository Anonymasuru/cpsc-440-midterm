# We're going to need to build this from the ground up.

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
    length = len(rs1)
    shifted = [0 for _ in range(length)]
    for i in range(length - n):
        shifted[i] = rs1[i + n]
    return shifted

def SRL(rs1, n):
    length = len(rs1)
    if n >= length:
        return [0 for _ in range(length)]
    shifted = [0 for _ in range(length)]
    for i in range(n, length):
        shifted[i] = rs1[i - n]
    return shifted

def SRA(rs1, n):
    length = len(rs1)
    sign_bit = rs1[0]
    if n >= length:
        return [sign_bit for _ in range(length)]
    shifted = [sign_bit for _ in range(length)]
    for i in range(n, length):
        shifted[i] = rs1[i - n]
    return shifted
def init_bitvector():
    bitvector = [0 for _ in range(32)] 
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
    # Initialize result as 32 zeros
    result = init_bitvector()
    # Initialize carry
    carry = 0
    for i in range(31, -1, -1):
        sum_bit, carry = full_adder(rs1[i], rs2[i], carry)
        result[i] = sum_bit
    # Flag checks
    N = result[0]                                                 # Negative flag
    Z = 1                                                         # Zero flag
    for bit in result:
        Z = AND(Z, XOR(bit, 1))               
    C = carry                                                     # Carry out of MSB
    V = AND(NOT(XOR(rs1[0], rs2[0])), XOR(result[0], rs1[0]))     # Overflow flag
    return result, {"N": N, "Z": Z, "C": C, "V": V}

def SUB(rs1, rs2):
    neg_rs2 = twos_complement(rs2)
    result, flags = ADD(rs1, neg_rs2)
    flags['C'] = XOR(flags['C'], 1)
    flags['V'] = AND(XOR(rs1[0], rs2[0]), XOR(result[0], rs1[0]))
    return result, flags

#===========
#MULTIPLIERS
#===========

def MUL(rs1, rs2):
    length = len(rs1)
    result = [0 for _ in range(length)]
    multiplicand = rs1[:]  # copy of rs1
    multiplier = rs2[:]    # copy of rs2

    for _ in range(length):
        # If the least significant bit of multiplier is 1, add multiplicand
        if multiplier[-1] == 1:
            result, _ = ADD(result, multiplicand)
        # Shift multiplicand left, multiplier right
        multiplicand = SLL(multiplicand)
        multiplier = SRL(multiplier, 1)
    return result

def MUL_signed(rs1, rs2):
    length = len(rs1)
    sign1 = rs1[0]
    sign2 = rs2[0]

    # Step 1: make copies
    a = rs1[:]
    b = rs2[:]

    # Step 2: take two’s complement if negative
    if sign1 == 1:
        a = twos_complement(a)
    if sign2 == 1:
        b = twos_complement(b)

    # Step 3: perform unsigned multiplication
    result = [0 for _ in range(length)]
    multiplicand = a[:]
    multiplier = b[:]
    for _ in range(length):
        if multiplier[-1] == 1:
            result, _ = ADD(result, multiplicand)
        multiplicand = SLL(multiplicand)
        multiplier = SRL(multiplier, 1)

    # Step 4: adjust sign if needed (negative result)
    if sign1 != sign2:
        result = twos_complement(result)

    return result

def DIV_signed(dividend, divisor):
    length = len(dividend)
    sign_dividend = dividend[0]
    sign_divisor = divisor[0]

    # Step 1: take absolute values
    a = dividend[:]
    b = divisor[:]
    if sign_dividend == 1:
        a = twos_complement(a)
    if sign_divisor == 1:
        b = twos_complement(b)

    # Step 2: perform unsigned division
    quotient, remainder = DIV_unsigned(a, b)

    # Step 3: adjust quotient sign
    if sign_dividend != sign_divisor:
        quotient = twos_complement(quotient)

    # Step 4: adjust remainder sign
    if sign_dividend == 1:
        remainder = twos_complement(remainder)

    return quotient, remainder

def DIV_unsigned(dividend, divisor):
    length = len(dividend)
    quotient = [0 for _ in range(length)]
    remainder = [0 for _ in range(length)]

    for i in range(length):
        # Shift left remainder and bring down next bit of dividend
        remainder = SLL(remainder, 1)
        remainder[-1] = dividend[i]

        # If remainder >= divisor, subtract divisor and set quotient bit
        temp_remainder, _ = SUB(remainder, divisor)
        if temp_remainder[0] == 0:  # No negative result
            remainder = temp_remainder
            quotient[i] = 1 

    return quotient, remainder

# test cases
# a = [0]*28 + [0,1,0,1]  # 5 in 32-bit
# b = [0]*28 + [0,1,1,0]  # 6 in 32-bit
# sum_result, sum_flags = ADD(a, b)
# print("\nAddition test")
# print(bits_to_str(a), "+", bits_to_str(b), "->", bits_to_str(sum_result), ";", sum_flags)
# sum_result, sum_flags = SUB(a, b)
# print("\nSubtraction test")
# print(bits_to_str(a), "-", bits_to_str(b), "->", bits_to_str(sum_result), ";", sum_flags)
# sum_result now contains 11 in 32-bit binary
# carry indicates overflow (1 if sum > 32 bits)

# I think these need to be done as rs1 and rs2 instead of a and b