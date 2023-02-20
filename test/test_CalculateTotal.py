import unittest
import os
import shutil

from . import *
import lib

class TestGetWishlistFilePath(unittest.TestCase):
    """ 
    Tests for 'get_wishlist_file_path'
    Most test are for when 'CalculateTotal' object is instantiated
    as the method 'get_wishlist_file_path' is called at that point.
    """
    temp_wishlist_text = lib.get_file_text(TEST_ASSETS_FILES_WISHLISTS[-1])
    temp_file_kwargs = dict(
            prefix='test_',
            suffix='.html', 
            dir='.',
            # dir=os.getcwd(),
            # text=temp_wishlist_text,
            mode='w+t',
            )

    def setUp(self) -> None:
        self.path = TEST_ASSETS_FILES_WISHLISTS[0]
        self.abs_path = lib.Path(self.path).absolute().__str__()

    def create_temp_wishlist_file(self, prefix=None, suffix='.html', dir="."):
        """ Create temporary wishlist file """
        mid = random_strings()
        prefix = prefix if isinstance(prefix, str) else ""
        suffix = suffix if isinstance(suffix, str) else ""
        filename = prefix + mid + suffix
        path = os.path.join(dir, filename) if isinstance(dir, str) else ""
        shutil.copy(TEST_ASSETS_FILES_WISHLISTS[0], path)
        return open(filename)
            

    def test_wishlist_in_class(self):
        """ Test with wishlist in the class/obj. """
        # Test if an absolute path is generated with object
        obj = lib.CalculateTotal(wishlist_path=self.path)
        msg = "{} | {}".format(self.path, obj.wishlist_path)
        self.assertEqual(obj.wishlist_path, self.abs_path, msg)
        
        store_wishlist_path = lib.CalculateTotal.wishlist_path
        obj = lib.CalculateTotal(self.path)
        msg = "{} | {}".format(self.path, obj.wishlist_path)
        self.assertEqual(obj.wishlist_path, self.abs_path, msg)
        # TearDown
        lib.CalculateTotal.wishlist_path = store_wishlist_path

    def test_wishlist_in_environment_variable(self):
        """ Set an environment variable and see if it is chosen. """
        try:
            # Set environment variable
            os.environ[WISHLIST_PATH_ENV_NAME] = TEST_ASSETS_FILES_WISHLISTS[0]
            obj = lib.CalculateTotal()
            self.assertEqual(obj.wishlist_path, TEST_ASSETS_FILES_WISHLISTS[0])
        finally:
            # Remove environment variable
            del os.environ[WISHLIST_PATH_ENV_NAME]
            assert bool(os.environ.get(WISHLIST_PATH_ENV_NAME)) is False, \
                "Environment Variable for temporary wishlist should be deleted to do proper testing."

    def test_wishlist_in_config_file(self):
        try:
            temp_wishlist_file = self.create_temp_wishlist_file()
            # Set config.py variable
            store_config_wishlist_path = lib.config.wishlist_path
            lib.config.wishlist_path = temp_wishlist_file.name
            obj = lib.CalculateTotal()
            self.assertEqual(obj.wishlist_path, temp_wishlist_file.name)
        finally:
            if os.path.exists(temp_wishlist_file.name):
                temp_wishlist_file.close()
                os.remove(temp_wishlist_file.name)
            # Restore config setting
            lib.config.wishlist_path = store_config_wishlist_path

    def test_wishlist_in_root(self):
        """ Create a wishlist in root and see if it is selected by CalculateTotal. """
        try:
            # Create wishlist file in present working directory
            temp_wishlist_file = self.create_temp_wishlist_file()
            obj = lib.CalculateTotal()
            self.assertEqual(obj.wishlist_path, temp_wishlist_file.name)
        finally:
            # Clean-up
            # Delete temporary wishlist
            if os.path.exists(temp_wishlist_file.name):
                temp_wishlist_file.close()
                os.remove(temp_wishlist_file.name)


class TestListRegexMatches(unittest.TestCase):
    pass