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

def test_twos_complement():
    assert alu.twos_complement([0,0,0,0]) == [1,1,1,1]
    assert alu.twos_complement([1,0,1,0]) == [0,1,1,0]
    assert alu.twos_complement([1,1,1,1]) == [0,0,0,1]
    assert alu.twos_complement([0,1,0,1]) == [1,1,1,1]

def test_bits_to_str():
    assert alu.bits_to_str([0,1,0,1]) == "0101"
    assert alu.bits_to_str([1,1,1,0]) == "1110"
    assert alu.bits_to_str([0,0,0,0]) == "0000"
    assert alu.bits_to_str([1,0,1,1]) == "1011"

def test_SLL():
    assert alu.SLL([1,0,1,0], 1) == [0,1,0,0]
    assert alu.SLL([1,1,0,0], 2) == [0,0,0,0]
    assert alu.SLL([0,1,1,1], 3) == [0,0,0,0]
    assert alu.SLL([1,0,0,1], 0) == [1,0,0,1]

def test_SRL():
    assert alu.SRL([1,0,1,0], 1) == [0,1,0,1]
    assert alu.SRL([1,1,0,0], 2) == [0,0,1,1]
    assert alu.SRL([0,1,1,1], 3) == [0,0,0,1]
    assert alu.SRL([1,0,0,1], 0) == [1,0,0,1]

def run_tests():
    test_AND()
    test_OR()
    test_XOR()
    test_NOT()
    test_twos_complement()
    test_bits_to_str()
    test_SLL()
    test_SRL()
    print("All tests passed!")

if __name__ == "__main__":
    run_tests()
