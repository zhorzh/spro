import unittest
import random
from functools import wraps


def with_chance(probability, default_value):
    if probability > 99 or probability < 1 or not isinstance(probability, int):
        raise TypeError

    def decorator(function):
        if not callable(function):
            raise TypeError

        @wraps(function)
        def wrapper(*args, **kwargs):
            if probability > random.randint(1, 98):
                return function(*args, **kwargs)
            else:
                return default_value
        return wrapper
    return decorator


class TestWithChance(unittest.TestCase):
    def test_dispersion(self):
        '''test probability by checking dispertion'''
        probability = 50

        def f():
            return True
        f = with_chance(probability, False)(f)

        # calculate dispersion
        iterations = 100000
        counter = 0.0
        for i in range(iterations):
            if f():
                counter += 1
        dispersion = probability - counter / iterations * 100

        # check if dispersion is less than 1%
        self.assertTrue(dispersion < 1.0)

    def test_function_return_proper_output(self):
        '''check if decorated function returns proper output'''
        def f():
            return True
        f = with_chance(50, False)(f)
        result = f()
        self.assertTrue(result in [True, False])

    def test_input_probability_is_valid(self):
        '''check if function raises error if probability is not valid'''
        def f():
            return True

        with self.assertRaises(TypeError):
            '''check if probability is <= 99'''
            f = with_chance(100, False)(f)
            f()
        with self.assertRaises(TypeError):
            '''check if probability is >= 1'''
            f = with_chance(0, False)(f)
            f()
        with self.assertRaises(TypeError):
            '''check if probability is integer'''
            f = with_chance(50.0, False)(f)
            f()

    def test_input_probability(self):
        '''check if function raises error if defined without attributes'''
        with self.assertRaises(TypeError):
            def f():
                return True
            f = with_chance()(f)

    def test_input_default_value(self):
        '''check if function raises error without default value'''
        with self.assertRaises(TypeError):
            def f():
                return True
            f = with_chance(50)(f)

    def test_decorator_recieves_function(self):
        '''check if decorator recieves a function'''
        with self.assertRaises(TypeError):
            f = 1
            f = with_chance(50, False)(f)

if __name__ == '__main__':
    unittest.main()
