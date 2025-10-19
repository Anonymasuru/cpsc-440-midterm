def bitwise_and(a, b):
    return [a[i] & b[i] for i in range(len(a))]

def bitwise_or(a, b):
    return [a[i] | b[i] for i in range(len(a))]

def bitwise_xor(a, b):
    return [a[i] ^ b[i] for i in range(len(a))]

def bitwise_not(a):
    return [1 - a[i] for i in range(len(a))]

def half_adder(a, b):
    sum_bit = a ^ b
    carry = a & b
    return sum_bit, carry

def full_adder(a, b, carry_in):
    sum1, carry1 = half_adder(a, b)
    sum2, carry2 = half_adder(sum1, carry_in)
    carry_out = carry1 | carry2
    return sum2, carry_out

def add_bitvectors(a, b):
    n = len(a)
    result = [0] * n
    carry = 0
    for i in reversed(range(n)):
        result[i], carry = full_adder(a[i], b[i], carry)
    return result, carry

def twos_complement(a):
    n = len(a)
    inverted = bitwise_not(a)
    one = [0]*(n-1) + [1]
    result, _ = add_bitvectors(inverted, one)
    return result

def sub_bitvectors(a, b):
    return add_bitvectors(a, twos_complement(b))

def logical_left_shift(a, k):
    n = len(a)
    return a[k:] + [0]*k

def logical_right_shift(a, k):
    n = len(a)
    return [0]*k + a[:n-k]

def arithmetic_right_shift(a, k):
    n = len(a)
    msb = a[0]
    return [msb]*k + a[:n-k]

a = [0,0,0,1,0,1,1,0]  # 22
b = [0,0,0,0,1,1,0,1]  # 13
sum_result, carry = add_bitvectors(a, b)
print("Sum:", sum_result, "Carry:", carry)
