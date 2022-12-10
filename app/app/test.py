'''Sample tests'''
from django.test import SimpleTestCase

from app import calc

'''
SimpleTestCase doesn't create test database
testsCase does
'''


class CalcTests(SimpleTestCase):

    '''Test calc module'''

    def test_add_numbers(self):
        '''Test adding numbers'''
        res = calc.add(5, 6)
        self.assertEqual(res, 11)

    def test_subtract_numbers(self):
        '''Test subtracting numbers'''
        res = calc.subtract(10, 5)
        self.assertEqual(res, 5)
