import unittest
import os

from PARAMS import *
from . import *
import lib


class TestFileExists(unittest.TestCase):

    def test_positive(self):
        """ Try a bunch of positive inputs. """
        for _input in FILES_EXISTS:
            self.assertTrue(lib.file_exists(_input), _input)

    def test_exception_quiet(self):
        """ Test alternative input values to see the response with and without quiet enabled. """
        for _input in (1, None, tuple()):
            self.assertFalse( lib.file_exists(_input,quiet=True) )
            with self.assertRaises(TypeError):
                lib.file_exists(_input, quiet=False)


class TestPathValidAbsolute(unittest.TestCase):

    def test_positive(self):
        """ Try a bunch of positive inputs. """
        for _input in FILES_EXISTS:
            abs_path = lib._path_valid_absolute(_input)
            isinstance(abs_path, str)
            # Testing if 'abs_path' is an absolute path
            self.assertTrue(os.path.isabs(abs_path), abs_path)

    def test_negative(self):
        """ Try a bunch or inputs that should return 'None'. """
        for _ in range(10):
            name = random_strings()
            self.assertEqual(lib._path_valid_absolute(name), None)


    def test_exception_quiet(self):
        """ Test alternative input values to see the response with and without quiet enabled. """
        for _input in (1, None, tuple()):
            self.assertFalse( lib._path_valid_absolute(_input,quiet=True) )
            with self.assertRaises(TypeError):
                lib._path_valid_absolute(_input, quiet=False)


class TestGetFileText(unittest.TestCase):
    def test_positive(self):
        """ Should return a valid string. """
        # FILES_EXISTS should have a bunch of text files.
        for _input in FILES_EXISTS:
            text = lib.get_file_text(_input)
            self.assertTrue(isinstance(text, str), _input)
            self.assertTrue(len(text) > 1e1, _input)


class TestValidWishlist(unittest.TestCase):
    def test_positive(self):
        """ Try a bunch of positive inputs. """
        input_texts = ((_path, lib.get_file_text(_path), ) for _path in TEST_ASSETS_FILES_WISHLISTS)
        for _path, _input_text in input_texts:
            # Verifying text 1st
            assert len(_input_text) > 1e4
            # Function test
            true = lib.valid_wishlist_text(_input_text)
            self.assertTrue(true, _path)
                

class TestGetWishlistFilesInDirectory(unittest.TestCase):
    def test_positive(self):
        val = lib.get_wishlist_files_in_directory(_test=True)
        assert isinstance(val, list), type(val)
        assert len(val) >= 2, val
        gen_type_str = (isinstance(path, str) for path in val)
        gen_ends_with_htm = (path.endswith('htm') or path.endswith('html') for path in val)
        assert all(gen_type_str)
        assert all(gen_ends_with_htm)

class TestGetXpathInText(unittest.TestCase):
    wishlist_path = TEST_ASSETS_FILES_WISHLISTS[0]
    wishlist_text = lib.get_file_text(wishlist_path)

    def test_positive(self):
        for _xpath in TEST_XPATH_MATCHES_PATTERNS:
            val = lib.get_xpath_in_text(_xpath, self.wishlist_text)
            # Test Output value
            assert isinstance(val, list), (type(val), _xpath)
            assert len(val) > 0, (_xpath, val)
            gen_type_str = (isinstance(path, str) for path in val)
            assert all(gen_type_str)

    def test_negative(self):
        """ Confirm that improper inputs results in errors. """
        inputs = (
            1,
            dict(),
            list(),
            tuple(),
            False,
        )
        # Test improper patterns 1st
        for _input in inputs:
            with self.assertRaises(TypeError):
                lib.get_xpath_in_text(_input, self.wishlist_text)
        # Now, test improper text value
        for _input in inputs:
            with self.assertRaises(TypeError):
                lib.get_xpath_in_text(XPATH_WHOLE_PRICE, _input)