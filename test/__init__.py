import unittest
import string
import random
import tempfile

import lib
from PARAMS import *


letters = string.ascii_letters
def random_strings(length=10):
    """ Generates a string of length of random characters. """
    return ''.join(random.choice(letters) for i in range(length))


class GenericTest(unittest.TestCase):

    def _test_positive(self):
        """ Try a bunch of positive inputs. """
        positive_container = tuple()
        for _input in positive_container:
            val = lib.path_valid_absolute(_input)
            isinstance(val, type)

    def _test_negative(self):
        """ Try a bunch of negative inputs. """
        negative_container = tuple()
        for _input in negative_container:
            val = lib.path_valid_absolute(_input)
            self.assertFalse(val == False)


    def _test_exception_quiet(self):
        """ Test alternative input values to see the response with and without quiet enabled. """
        for _input in (1, None, tuple(), ):
            self.assertFalse( lib.path_valid_absolute(_input,quiet=True) )
            with self.assertRaises(TypeError):
                lib.path_valid_absolute(_input, quiet=False)