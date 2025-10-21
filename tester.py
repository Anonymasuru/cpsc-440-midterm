import arithmetic_logic_unit as alu

def test_AND():
    assert alu.AND(0, 0) == 0
    assert alu.AND(0, 1) == 0
    assert alu.AND(1, 0) == 0
    assert alu.AND(1, 1) == 1

def test_OR():
    assert alu.OR(0, 0) == 0
    assert alu.OR(0, 1) == 1
    assert alu.OR(1, 0) == 1
    assert alu.OR(1, 1) == 1

def test_XOR():
    assert alu.XOR(0, 0) == 0
    assert alu.XOR(0, 1) == 1
    assert alu.XOR(1, 0) == 1
    assert alu.XOR(1, 1) == 0

def test_NOT():
    assert alu.NOT(0) == 1
    assert alu.NOT(1) == 0

# def test_twos_complement():
#     assert alu.twos_complement([0,0,0,0]) == [1,1,1,1]
#     assert alu.twos_complement([1,0,1,0]) == [0,1,1,0]
#     assert alu.twos_complement([1,1,1,1]) == [0,0,0,1]
#     assert alu.twos_complement([0,1,0,1]) == [1,1,1,1]

def test_shift():
    bv_pos = [0]*24 + [0,1,0,1,1,0,0,1]
    bv_neg = [1] + [0]*23 + [0,1,1,0,0,1,0]

    # SLL tests
    print("\n Shifter test")
    print(alu.bits_to_str(bv_pos), "-> shift left by one ->", alu.bits_to_str(alu.SLL(bv_pos, 1)))
    assert alu.SLL(bv_pos, 1) == bv_pos[1:] + [0]
    assert alu.SLL(bv_pos, 3) == bv_pos[3:] + [0,0,0]
    assert alu.SLL(bv_pos, 0) == bv_pos
    assert alu.SLL(bv_pos, 32) == [0]*32

    # SRL tests
    assert alu.SRL(bv_pos, 1) == [0] + bv_pos[:-1]
    assert alu.SRL(bv_pos, 3) == [0,0,0] + bv_pos[:-3]
    assert alu.SRL(bv_pos, 0) == bv_pos
    assert alu.SRL(bv_pos, 32) == [0]*32

    # SRA tests
    msb_pos = bv_pos[0]
    msb_neg = bv_neg[0]

    # Shift by 1
    assert alu.SRA(bv_neg, 1) == [msb_neg] + bv_neg[:-1]
    assert alu.SRA(bv_pos, 1) == [msb_pos] + bv_pos[:-1]

    # Shift by 3
    assert alu.SRA(bv_neg, 3) == [msb_neg]*3 + bv_neg[:-3]

    # Shift by 0
    assert alu.SRA(bv_pos, 0) == bv_pos

    print("All 32-bit shift tests passed!")

def test_ALU():
    # test cases
    a = [0]*28 + [0,1,0,1]  # 5 in 32-bit
    b = [0]*28 + [0,1,1,0]  # 6 in 32-bit
    print("\nAddition test")
    sum_result, sum_flags = alu.ADD(a, b)
    print(alu.bits_to_str(a), "+", alu.bits_to_str(b), "->", alu.bits_to_str(sum_result), ";", sum_flags)
    print("\nSubtraction test")
    sum_result, sum_flags = alu.SUB(a, b)
    print(alu.bits_to_str(a), "-", alu.bits_to_str(b), "->", alu.bits_to_str(sum_result), ";", sum_flags)
    print("\nMUL test")
    sum_result, sum_flags = alu.MUL(a, b)
    print(alu.bits_to_str(a), "*", alu.bits_to_str(b), "->", alu.bits_to_str(sum_result), ";", sum_flags)

    # sum_result now contains 11 in 32-bit binary
    # carry indicates overflow (1 if sum > 32 bits)

def run_tests():
    print("\nLogical operator test")
    test_AND()
    test_OR()
    test_XOR()
    test_NOT()
    print("All logical operator tests passed")
    test_ALU()
    test_shift()
    # test_twos_complement()
    # test_bits_to_str()
    # test_SLL()
    # test_SRL()
    print("All tests passed!")

if __name__ == "__main__":
    run_tests()
