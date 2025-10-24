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
    one = init_bitvector_one()
    result, _ = ADD(inverted, one)
    return result

def bits_to_str(bits):
    XLEN = len(bits)
    chunks = [''.join(str(bits[i:i+8][j]) for j in range(8)) for i in range(0, XLEN, 8)]
    return '_'.join(chunks)

def str_to_bits(bitstr):
    # Remove underscores and convert each character to int
    return [int(c) for c in bitstr.replace('_', '')]

def init_bitvector():
    bitvector = [0 for _ in range(XLEN)] 
    return bitvector

def init_bitvector_one():
    bitvector = init_bitvector()
    bitvector[-1] = 1
    return bitvector

def inc_one(bits):
    inc = init_bitvector_one()
    result, _ = ADD(bits, inc)
    return result

def dec_one(bits):
    dec = init_bitvector_one()
    result, _ = SUB(bits, dec)
    return result

def compare_bitvectors_gt(a, b):
    diff, _ = SUB(a, b)
    result_sign = diff[0]
    return 0 if result_sign == 1 else 1


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
    if neg_dividend == 1:
        remainder = twos_complement(remainder)

    remainder_flag = remainder[-1]

    return quotient, remainder_flag

#==================
#IEE-754 OPERATIONS
#==================

def unpack_32(bits):
    sign = [bits[0]]       
    exp = bits[1:9] 
    frac = bits[9:]
    return sign, exp, frac

def pack_32(sign, exp, frac):
    bits = sign + exp + frac
    return bits

def init_bitvector_max_exp():
    return [1,1,1,1,1,1,1,0]  # 254

def init_bitvector_zero_exp():
    bitvector = [0 for _ in range(8)] 
    return bitvector


def normalize(mant, exp):
    overflow = 0
    underflow = 0

    # Overflow: MSB > 1 (extra leading bit)
    if mant[0] == 1 and len(mant) > 1:
        mant = SRL(mant, 1)
        exp = inc_one(exp)
        # Check if exponent overflowed
        if compare_bitvectors_gt(exp, init_bitvector_max_exp()):  # 255 for 8-bit
            overflow = 1

    # Underflow: first bit is 0 (after subtraction)
    while mant[0] == 0:
        mant = SLL(mant, 1)
        exp = dec_one(exp)
        # Check if exponent reached zero
        if compare_bitvectors_gt(init_bitvector_zero_exp(), exp) == 1:
            underflow = 1
            break

    return mant, exp, overflow, underflow


def round_mantissa(mant):
    fraction_len = 23
    # extra bits beyond fraction
    extra_bits = mant[fraction_len+1:]
    round_bit = mant[fraction_len]
    sticky_bit = 0
    for b in extra_bits:
        sticky_bit = OR(sticky_bit, b)  # sticky = 1 if any lower bit is 1

    # Determine if we need to increment mantissa
    if round_bit == 1 and OR(sticky_bit, mant[fraction_len-1]) == 1:
        mant = inc_one(mant[:fraction_len+1]) + mant[fraction_len+1:]  # increment upper part
    else:
        mant = mant[:fraction_len+1]  # truncate extra bits

    return mant

def fadd_32(a, b):
    # Step 1: Unpack operands
    sign_a, exp_a, frac_a = unpack_32(a)
    sign_b, exp_b, frac_b = unpack_32(b)

    # Step 2: Handle denormalized numbers (no implicit 1 if exponent is 0)
    if compare_bitvectors_gt(exp_a, init_bitvector_zero_exp()):
        mant_a = [1] + frac_a[:]
    else:
        mant_a = frac_a[:]

    if compare_bitvectors_gt(exp_b, init_bitvector_zero_exp()):
        mant_b = [1] + frac_b[:]
    else:
        mant_b = frac_b[:]

    # Step 3: Align exponents
    while compare_bitvectors_gt(exp_b, exp_a):
        mant_a = SRL(mant_a, 1)
        exp_a = inc_one(exp_a)
    while compare_bitvectors_gt(exp_a, exp_b):
        mant_b = SRL(mant_b, 1)
        exp_b = inc_one(exp_b)

    # Step 4: Add or subtract mantissas depending on signs
    if sign_a == sign_b:
        mant_sum, _ = ADD(mant_a, mant_b)
        result_sign = sign_a
    else:
        if compare_bitvectors_gt(mant_a, mant_b):
            mant_sum, _ = SUB(mant_a, mant_b)
            result_sign = sign_a
        else:
            mant_sum, _ = SUB(mant_b, mant_a)
            result_sign = sign_b

    # Step 5: Normalize mantissa and adjust exponent
    mant_sum, exp_a, overflow, underflow = normalize(mant_sum, exp_a)

    # Step 6: Rounding
    mant_sum = round_mantissa(mant_sum)

    # Step 7: Handle special cases
    # Overflow → set to Inf
    if overflow:
        exp_a = init_bitvector_max_exp()
        mant_sum = [0]*len(mant_sum)

    # Underflow → set to zero
    if underflow:
        mant_sum = [0]*len(mant_sum)
        exp_a = init_bitvector_zero_exp()
        result_sign = 0  # +0

    # Step 8: Pack result (drop implicit 1 if normalized)
    if compare_bitvectors_gt(exp_a, init_bitvector_zero_exp()):
        result_bits = pack_32([result_sign], exp_a, mant_sum[1:])
    else:
        result_bits = pack_32([result_sign], exp_a, mant_sum[:])

    return result_bits, overflow, underflow

def fsub_32(a, b):
    # Step 1: Flip the sign of b
    sign_b, exp_b, frac_b = unpack_32(b)
    flipped_sign_b = [XOR(sign_b[0], 1)]  # 0->1, 1->0
    b_flipped = pack_32(flipped_sign_b, exp_b, frac_b)

    # Step 2: Use fadd_32 on a and -b
    result_bits, overflow, underflow = fadd_32(a, b_flipped)

    return result_bits, overflow, underflow

def fmul_32(a, b):
    # Step 1: Unpack operands
    sign_a, exp_a, frac_a = unpack_32(a)
    sign_b, exp_b, frac_b = unpack_32(b)

    # Step 2: Determine result sign
    result_sign = XOR(sign_a[0], sign_b[0])

    # Step 3: Handle zero operands early
    zero_exp = init_bitvector_zero_exp()
    zero_frac = [0]*len(frac_a)
    if exp_a == zero_exp and all(bit == 0 for bit in frac_a):
        return pack_32([result_sign], zero_exp, zero_frac), 0, 0
    if exp_b == zero_exp and all(bit == 0 for bit in frac_b):
        return pack_32([result_sign], zero_exp, zero_frac), 0, 0

    # Step 4: Add implicit 1 for normalized numbers
    if compare_bitvectors_gt(exp_a, zero_exp):
        mant_a = [1] + frac_a[:]
    else:
        mant_a = frac_a[:]
    if compare_bitvectors_gt(exp_b, zero_exp):
        mant_b = [1] + frac_b[:]
    else:
        mant_b = frac_b[:]

    # Step 5: Multiply mantissas using bitvector MUL
    mant_product, mul_flags = MUL(mant_a, mant_b)
    overflow = 0
    underflow = 0
    if mul_flags["overflow"] == 1:
        overflow = 1

    # Step 6: Exponent addition with bias subtraction
    bias = init_bitvector_from_int(127)  # bias for single-precision
    temp_exp, _ = ADD(exp_a, exp_b)
    result_exp, _ = SUB(temp_exp, bias)

    # Step 7: Normalize mantissa
    # If MSB of product is 1 (overflow from multiply), shift right
    if mant_product[0] == 1:
        mant_product = SRL(mant_product, 1)
        result_exp = inc_one(result_exp)
        if compare_bitvectors_gt(result_exp, init_bitvector_max_exp()):
            overflow = 1
    # If MSB = 0, shift left until normalized
    while mant_product[0] == 0:
        mant_product = SLL(mant_product, 1)
        result_exp = dec_one(result_exp)
        if compare_bitvectors_gt(zero_exp, result_exp) == 1:
            underflow = 1
            break

    # Step 8: Round mantissa (approximate round-to-nearest-even)
    mant_product = round_mantissa(mant_product)

    # Step 9: Handle special cases
    if overflow:
        result_exp = init_bitvector_max_exp()
        mant_product = [0]*len(mant_product)
    if underflow:
        result_exp = zero_exp
        mant_product = [0]*len(mant_product)
        result_sign = 0  # +0

    # Step 10: Pack final result
    if compare_bitvectors_gt(result_exp, zero_exp):
        result_bits = pack_32([result_sign], result_exp, mant_product[1:])  # drop implicit 1
    else:
        result_bits = pack_32([result_sign], result_exp, mant_product[:])   # denormal

    return result_bits, overflow, underflow