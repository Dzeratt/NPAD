class IncorrectTriangleSides(Exception):
    pass

def get_triangle_type(a, b, c):

    if a <= 0 or b <= 0 or c <= 0 or a + b <= c or a + c <= b or b + c <= a:
        raise IncorrectTriangleSides('IncorrectTriangleSides')

    if a == b == c:
        return "equilateral"
    elif a == b or b == c or a == c:
        return "isosceles"
    else:
        return "nonequilateral"


if __name__ == "__main__":
    try:
        print(get_triangle_type(3, 3, 3))
        print(get_triangle_type(2, 2, 3))
        print(get_triangle_type(4, 4, 2))
        print(get_triangle_type(5, 3, 5))
        print(get_triangle_type(3, 4, 5))
        print(get_triangle_type(5, 7, 10))
        print(get_triangle_type(0, 1, 1))
        print(get_triangle_type(-1, 2, 2))
        print(get_triangle_type(1, 2, 3))
        print(get_triangle_type(1, 1, 2))
        print(get_triangle_type(0, 0, 0))
        print(get_triangle_type(-3, -4, 5))
    except IncorrectTriangleSides as e:
        print(e)
