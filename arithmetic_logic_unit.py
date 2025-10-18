# We're going to need to build this from the ground up.

# These operators appear to go through the entire array and produce results based on their logic criteria

# if both inputs are on
def AND(a, b): 
    result = []
    for i in range(len(a)):
        if a[i] == 1 and b[i] == 1:
            result.append(1)
        else:
            result.append(0)
    return result

# if one input is on
def OR(a, b): 
    result = []
    for i in range(len(a)):
        if a[i] == 1 or b[i] == 1:
            result.append(1)
        else:
            result.append(0)
    return result

# if inputs are different
def XOR(a, b): 
    result = []
    for i in range(len(a)):
        if a[i] != b[i]:
            result.append(1)
        else:
            result.append(0)
    return result

# essentially flips the bit
def NOT(a):
    result = []
    for bit in a:
        if bit == 0:
            result.append(1)
        else:
            result.append(0)
    return result

def twos_complement(a):
    inverted = NOT(a)
    one = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
    result, _ = ADD(inverted, one)
    return result

def bits_to_str(bits):
    return ''.join(str(b) for b in bits)


#======
#ADDERS
#======

def half_adder(a, b):
    # sum is 1 if exactly one of a, b is 1
    if a == b:
        sum_bit = 0
    else:
        sum_bit = 1

    # carry is 1 only if both a and b are 1
    if a == 1 and b == 1:
        carry = 1
    else:
        carry = 0

    return sum_bit, carry

def full_adder(a, b, carry_in):
    # first half adder
    sum1, carry1 = half_adder(a, b)
    
    # second half adder with carry_in
    sum2, carry2 = half_adder(sum1, carry_in)
    
    # final carry-out: 1 if either carry1 or carry2 is 1
    if carry1 == 1 or carry2 == 1:
        carry_out = 1
    else:
        carry_out = 0

    return sum2, carry_out

def ADD(rs1, rs2):

    # Initialize result as 32 zeros
    result = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    
    # Initialize carry
    carry = 0

    # -----------------------------
    # Repeat addition logic 32 times
    # -----------------------------

    sum_bit, carry = full_adder(rs1[31], rs2[31], carry) # B0 (LSB)
    result[31] = sum_bit
    sum_bit, carry = full_adder(rs1[30], rs2[30], carry)
    result[30] = sum_bit
    sum_bit, carry = full_adder(rs1[29], rs2[29], carry)
    result[29] = sum_bit
    sum_bit, carry = full_adder(rs1[28], rs2[28], carry)
    result[28] = sum_bit
    sum_bit, carry = full_adder(rs1[27], rs2[27], carry)
    result[27] = sum_bit
    sum_bit, carry = full_adder(rs1[26], rs2[26], carry)
    result[26] = sum_bit
    sum_bit, carry = full_adder(rs1[25], rs2[25], carry)
    result[25] = sum_bit
    sum_bit, carry = full_adder(rs1[24], rs2[24], carry)
    result[24] = sum_bit
    sum_bit, carry = full_adder(rs1[23], rs2[23], carry)
    result[23] = sum_bit
    sum_bit, carry = full_adder(rs1[22], rs2[22], carry)
    result[22] = sum_bit
    sum_bit, carry = full_adder(rs1[21], rs2[21], carry)
    result[21] = sum_bit
    sum_bit, carry = full_adder(rs1[20], rs2[20], carry)
    result[20] = sum_bit
    sum_bit, carry = full_adder(rs1[19], rs2[19], carry)
    result[19] = sum_bit
    sum_bit, carry = full_adder(rs1[18], rs2[18], carry)
    result[18] = sum_bit
    sum_bit, carry = full_adder(rs1[17], rs2[17], carry)
    result[17] = sum_bit
    sum_bit, carry = full_adder(rs1[16], rs2[16], carry)
    result[16] = sum_bit
    sum_bit, carry = full_adder(rs1[15], rs2[15], carry)
    result[15] = sum_bit
    sum_bit, carry = full_adder(rs1[14], rs2[14], carry)
    result[14] = sum_bit
    sum_bit, carry = full_adder(rs1[13], rs2[13], carry)
    result[13] = sum_bit
    sum_bit, carry = full_adder(rs1[12], rs2[12], carry)
    result[12] = sum_bit
    sum_bit, carry = full_adder(rs1[11], rs2[11], carry)
    result[11] = sum_bit
    sum_bit, carry = full_adder(rs1[10], rs2[10], carry)
    result[10] = sum_bit
    sum_bit, carry = full_adder(rs1[9], rs2[9], carry)
    result[9] = sum_bit
    sum_bit, carry = full_adder(rs1[8], rs2[8], carry)
    result[8] = sum_bit
    sum_bit, carry = full_adder(rs1[7], rs2[7], carry)
    result[7] = sum_bit
    sum_bit, carry = full_adder(rs1[6], rs2[6], carry)
    result[6] = sum_bit
    sum_bit, carry = full_adder(rs1[5], rs2[5], carry)
    result[5] = sum_bit
    sum_bit, carry = full_adder(rs1[4], rs2[4], carry)
    result[4] = sum_bit
    sum_bit, carry = full_adder(rs1[3], rs2[3], carry)
    result[3] = sum_bit
    sum_bit, carry = full_adder(rs1[2], rs2[2], carry)
    result[2] = sum_bit
    sum_bit, carry = full_adder(rs1[1], rs2[1], carry)
    result[1] = sum_bit
    sum_bit, carry = full_adder(rs1[0], rs2[0], carry) # B31 (MSB)
    result[0] = sum_bit

    # Flag checks
    N = result[0] # Negative flag
    Z = 1 if all(bit == 0 for bit in result) else 0  # Zero flag
    C = carry                              # Carry out of MSB
    V = 1 if (rs1[0] == rs2[0]) and (result[0] != rs1[0]) else 0 # Signed overflow
    
    return result, {"N": N, "Z": Z, "C": C, "V": V}


def SUB(rs1, rs2):
    neg_rs2 = twos_complement(rs2)
    result, flags = ADD(rs1, neg_rs2)
    flags['C'] = 1 - flags['C']
    flags['V'] = 1 if (rs1[0] != rs2[0]) and (result[0] != rs1[0]) else 0
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