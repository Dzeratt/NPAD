class IncorrectTriangleSides(Exception):
    pass


class Triangle:
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

        if not self._is_valid_triangle():
            raise IncorrectTriangleSides('IncorrectTriangleSides')

    def _is_valid_triangle(self):
        return self.a > 0 and self.b > 0 and self.c > 0 and \
               self.a + self.b > self.c and \
               self.a + self.c > self.b and \
               self.b + self.c > self.a

    def triangle_type(self):
        if self.a == self.b == self.c:
            return "equilateral"
        elif self.a == self.b or self.b == self.c or self.a == self.c:
            return "isosceles"
        else:
            return "nonequilateral"

    def perimeter(self):
        return self.a + self.b + self.c


if __name__ == "__main__":
    try:
        t1 = Triangle(3, 3, 3)
        print(t1.triangle_type())
        print(t1.perimeter())

        t2 = Triangle(2, 2, 3)
        print(t2.triangle_type())
        print(t2.perimeter())

        t3 = Triangle(3, 4, 5)
        print(t3.triangle_type())
        print(t3.perimeter())

        t4 = Triangle(0, 1, 1)
    except IncorrectTriangleSides as e:
        print(e)
