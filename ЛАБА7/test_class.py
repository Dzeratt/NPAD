import pytest
from triangle_class import Triangle, IncorrectTriangleSides


def test_equilateral_triangle():
    t = Triangle(3, 3, 3)
    assert t.triangle_type() == "equilateral"
    assert t.perimeter() == 9


def test_isosceles_triangle():
    t1 = Triangle(2, 2, 3)
    assert t1.triangle_type() == "isosceles"
    assert t1.perimeter() == 7

    t2 = Triangle(4, 4, 2)
    assert t2.triangle_type() == "isosceles"
    assert t2.perimeter() == 10

    t3 = Triangle(5, 3, 5)
    assert t3.triangle_type() == "isosceles"
    assert t3.perimeter() == 13


def test_nonequilateral_triangle():
    t1 = Triangle(3, 4, 5)
    assert t1.triangle_type() == "nonequilateral"
    assert t1.perimeter() == 12

    t2 = Triangle(5, 7, 10)
    assert t2.triangle_type() == "nonequilateral"
    assert t2.perimeter() == 22


def test_incorrect_sides_zero():
    with pytest.raises(IncorrectTriangleSides):
        Triangle(0, 1, 1)


def test_incorrect_sides_negative():
    with pytest.raises(IncorrectTriangleSides):
        Triangle(-1, 2, 2)


def test_incorrect_sides_sum_less_than_third():
    with pytest.raises(IncorrectTriangleSides):
        Triangle(1, 2, 3)


def test_incorrect_sides_sum_equal_to_third():
    with pytest.raises(IncorrectTriangleSides):
        Triangle(1, 1, 2)


def test_incorrect_sides_all_zero():
    with pytest.raises(IncorrectTriangleSides):
        Triangle(0, 0, 0)


def test_incorrect_sides_two_negative():
    with pytest.raises(IncorrectTriangleSides):
        Triangle(-3, -4, 5)


if __name__ == "__main__":
    pytest.main()
