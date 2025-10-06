import pytest
from calc import add, subtract, divide

def test_add():
    """
    Test the add function with positive and negative values.
    """
    assert add(2, 3) == 5
    assert add(-1, 1) == 0

def test_subtract():
    """
    Test the subtract function with positive and negative results.
    """
    assert subtract(5, 2) == 3
    assert subtract(0, 3) == -3

def test_divide():
    """
    Test the divide function with valid inputs.
    """
    assert divide(10, 2) == 5

def test_divide_by_zero():
    """
    Test that divide function raises ZeroDivisionError when dividing by zero.
    """
    with pytest.raises(ZeroDivisionError):
        divide(5, 0)
