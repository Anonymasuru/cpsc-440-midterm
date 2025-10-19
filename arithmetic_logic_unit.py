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

#========
#SHIFTERS
#========

def SLL(bits, amount):
    width = len(bits)
    
    # 1. Slice off the leftmost `amount` bits
    shifted_part = bits[amount:]  # bits that remain after shift
    
    # 2. Build zeros to fill the right
    zeros = init_bitvector()
    
    # 3. Concatenate
    result = shifted_part + zeros
    
    # 4. Ensure result is same width (optional)
    if len(result) > width:
        result = result[:width]
    
    return result

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

# test cases
a = [0]*28 + [0,1,0,1]  # 5 in 32-bit
b = [0]*28 + [0,1,1,0]  # 6 in 32-bit
sum_result, sum_flags = ADD(a, b)
print("\nAddition test")
print(bits_to_str(a), "+", bits_to_str(b), "->", bits_to_str(sum_result), ";", sum_flags)
sum_result, sum_flags = SUB(a, b)
print("\nSubtraction test")
print(bits_to_str(a), "-", bits_to_str(b), "->", bits_to_str(sum_result), ";", sum_flags)
# sum_result now contains 11 in 32-bit binary
# carry indicates overflow (1 if sum > 32 bits)

# I think these need to be done as rs1 and rs2 instead of a and b