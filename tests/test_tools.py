from cal.tools.math_tools import add_numbers, sub_numbers

def test_add_numbers():
    assert add_numbers.func(2, 3) == 5

def test_sub_numbers():
    assert sub_numbers.func(9, 2) == 7