import unittest
from triangle_func import get_triangle_type, IncorrectTriangleSides


class TestGetTriangleType(unittest.TestCase):

    def test_equilateral_triangle(self):
        self.assertEqual(get_triangle_type(3, 3, 3), "equilateral")

    def test_isosceles_triangle(self):
        self.assertEqual(get_triangle_type(2, 2, 3), "isosceles")
        self.assertEqual(get_triangle_type(4, 4, 2), "isosceles")
        self.assertEqual(get_triangle_type(5, 3, 5), "isosceles")

    def test_nonequilateral_triangle(self):
        self.assertEqual(get_triangle_type(3, 4, 5), "nonequilateral")
        self.assertEqual(get_triangle_type(5, 7, 10), "nonequilateral")

    def test_incorrect_sides_zero(self):
        with self.assertRaises(IncorrectTriangleSides):
            get_triangle_type(0, 1, 1)

    def test_incorrect_sides_negative(self):
        with self.assertRaises(IncorrectTriangleSides):
            get_triangle_type(-1, 2, 2)

    def test_incorrect_sides_sum_less_than_third(self):
        with self.assertRaises(IncorrectTriangleSides):
            get_triangle_type(1, 2, 3)

    def test_incorrect_sides_sum_equal_to_third(self):
        with self.assertRaises(IncorrectTriangleSides):
            get_triangle_type(1, 1, 2)

    def test_incorrect_sides_all_zero(self):
        with self.assertRaises(IncorrectTriangleSides):
            get_triangle_type(0, 0, 0)

    def test_incorrect_sides_two_negative(self):
        with self.assertRaises(IncorrectTriangleSides):
            get_triangle_type(-3, -4, 5)


if __name__ == "__main__":
    unittest.main()
