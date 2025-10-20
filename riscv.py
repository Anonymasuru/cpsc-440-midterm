# Keeping for reference to make shifers

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
