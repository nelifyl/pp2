class Math:

    @classmethod
    def add(cls, a, b):
        return a + b

    @classmethod
    def multiply(cls, a, b):
        return a * b

    @classmethod
    def square(cls, x):
        return x * x

    @classmethod
    def cube(cls, x):
        return x ** 3

    @classmethod
    def is_even(cls, x):
        return x % 2 == 0