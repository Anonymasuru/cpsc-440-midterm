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

#Addition
def ADD(a, b):

    # Initialize result as 32 zeros
    result = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    
    # Initialize carry
    carry = 0

    # -----------------------------
    # Repeat addition logic 32 times
    # -----------------------------

    sum_bit, carry = full_adder(a[31], b[31], carry) # B0 (LSB)
    result[31] = sum_bit
    sum_bit, carry = full_adder(a[30], b[30], carry)
    result[30] = sum_bit
    sum_bit, carry = full_adder(a[29], b[29], carry)
    result[29] = sum_bit
    sum_bit, carry = full_adder(a[28], b[28], carry)
    result[28] = sum_bit
    sum_bit, carry = full_adder(a[27], b[27], carry)
    result[27] = sum_bit
    sum_bit, carry = full_adder(a[26], b[26], carry)
    result[26] = sum_bit
    sum_bit, carry = full_adder(a[25], b[25], carry)
    result[25] = sum_bit
    sum_bit, carry = full_adder(a[24], b[24], carry)
    result[24] = sum_bit
    sum_bit, carry = full_adder(a[23], b[23], carry)
    result[23] = sum_bit
    sum_bit, carry = full_adder(a[22], b[22], carry)
    result[22] = sum_bit
    sum_bit, carry = full_adder(a[21], b[21], carry)
    result[21] = sum_bit
    sum_bit, carry = full_adder(a[20], b[20], carry)
    result[20] = sum_bit
    sum_bit, carry = full_adder(a[19], b[19], carry)
    result[19] = sum_bit
    sum_bit, carry = full_adder(a[18], b[18], carry)
    result[18] = sum_bit
    sum_bit, carry = full_adder(a[17], b[17], carry)
    result[17] = sum_bit
    sum_bit, carry = full_adder(a[16], b[16], carry)
    result[16] = sum_bit
    sum_bit, carry = full_adder(a[15], b[15], carry)
    result[15] = sum_bit
    sum_bit, carry = full_adder(a[14], b[14], carry)
    result[14] = sum_bit
    sum_bit, carry = full_adder(a[13], b[13], carry)
    result[13] = sum_bit
    sum_bit, carry = full_adder(a[12], b[12], carry)
    result[12] = sum_bit
    sum_bit, carry = full_adder(a[11], b[11], carry)
    result[11] = sum_bit
    sum_bit, carry = full_adder(a[10], b[10], carry)
    result[10] = sum_bit
    sum_bit, carry = full_adder(a[9], b[9], carry)
    result[9] = sum_bit
    sum_bit, carry = full_adder(a[8], b[8], carry)
    result[8] = sum_bit
    sum_bit, carry = full_adder(a[7], b[7], carry)
    result[7] = sum_bit
    sum_bit, carry = full_adder(a[6], b[6], carry)
    result[6] = sum_bit
    sum_bit, carry = full_adder(a[5], b[5], carry)
    result[5] = sum_bit
    sum_bit, carry = full_adder(a[4], b[4], carry)
    result[4] = sum_bit
    sum_bit, carry = full_adder(a[3], b[3], carry)
    result[3] = sum_bit
    sum_bit, carry = full_adder(a[2], b[2], carry)
    result[2] = sum_bit
    sum_bit, carry = full_adder(a[1], b[1], carry)
    result[1] = sum_bit
    sum_bit, carry = full_adder(a[0], b[0], carry) # B31 (MSB)
    result[0] = sum_bit

    # Flag checks
    N = result[0] # Negative flag
    Z = 1 if all(bit == 0 for bit in result) else 0  # Zero flag
    C = carry                              # Carry out of MSB
    V = 1 if (a[0] == b[0]) and (result[0] != a[0]) else 0 # Signed overflow
    
    return result, {"N": N, "Z": Z, "C": C, "V": V}

#Subtraction
def SUB(a, b):
    neg_b = twos_complement(b)
    result, flags = ADD(a, neg_b)
    flags['C'] = 1 - flags['C']
    flags['V'] = 1 if (a[0] != b[0]) and (result[0] != a[0]) else 0
    return result, flags

# test cases
a = [0]*28 + [0,1,0,1]  # 5 in 32-bit
b = [0]*28 + [0,1,1,0]  # 6 in 32-bit
sum_result, sum_flags = ADD(a, b)
print("Addition test")
print(bits_to_str(a), "+", bits_to_str(b), "->", bits_to_str(sum_result), ";", sum_flags)
sum_result, sum_flags = SUB(a, b)
print("\nSubtraction test")
print(bits_to_str(a), "-", bits_to_str(b), "->", bits_to_str(sum_result), ";", sum_flags)
# sum_result now contains 11 in 32-bit binary
# carry indicates overflow (1 if sum > 32 bits)
