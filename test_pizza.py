import pytest
from pizza import *


def test_other_size_init():
    with pytest.raises(ValueError):
        pizza = Pepperoni(size='M')


def test_other_size_setter():
    with pytest.raises(ValueError):
        pizza = Pepperoni(size='L')
        pizza.size = 'M'


def test_good_size_setter():
    pizza = Pepperoni(size='L')
    pizza.size = 'XL'
    assert pizza.size == 'XL'


def test_equality():
    assert Pepperoni() == Pepperoni()


def test_inequality():
    assert Margherita() != Hawaiian()


def test_inequality_to_int():
    assert Margherita() != 3


def test_str():
    assert isinstance(str(Pepperoni()), str)


def test_inequality_sizes():
    assert Margherita(size='L') != Margherita(size='XL')


def test_dict():
    assert isinstance(Pepperoni().dict(), dict)


def test_bake_pickup_deliver_type():
    assert (bake() is None) & (pickup() is None) & (deliver() is None)
