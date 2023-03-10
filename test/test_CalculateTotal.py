import unittest
import os
import shutil
import sys, io

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


class TestWishlistRegexMatches(unittest.TestCase):
    wishlist_path = TEST_ASSETS_FILES_WISHLISTS[0]

    def test_positive(self):
        """ Ensure that regex patterns works on wishlist HTML text. """
        obj = lib.CalculateTotal(self.wishlist_path)
        for patt in TEST_REGEX_MATCHES_PATTERNS:
            # Function
            sub_texts = obj.wishlist_regex_matches(patt)
            # Assert output type
            assert isinstance(sub_texts, list), type(sub_texts)
            assert len(sub_texts) > 0, patt
            # Assert each element of sub_texts is a str
            gen_is_strs = (isinstance(sub_text, str) for sub_text in sub_texts)
            sub_text_and_type_pairs = tuple((sub_text,type(sub_text)) for sub_text in sub_texts)
            assert all(gen_is_strs), \
                (sub_text_and_type_pairs[:5], "And there is more. The following is the regex pattern", patt)
            # Assert each element of sub_text is a str of length
            gen_is_str_length = (len(sub_text) > 0 for sub_text in sub_texts)
            sub_text_and_len = tuple((sub_text,len(sub_text)) for sub_text in sub_texts)
            assert all(gen_is_str_length), \
                (sub_text_and_len[:5], "And there is more. The following is the regex pattern", patt)


class TestListXpathMatches(unittest.TestCase):
    wishlist_path = TEST_ASSETS_FILES_WISHLISTS[0]
    
    def test_positive(self):
        """ Ensure that xpath patterns works on wishlist HTML text. """
        obj = lib.CalculateTotal(self.wishlist_path)
        for xpath in TEST_XPATH_MATCHES_PATTERNS:
            # Function
            sub_texts = obj.wishlist_xpath_matches(xpath)
            # Assert output type
            assert isinstance(sub_texts, list), type(sub_texts)
            assert len(sub_texts) > 0, xpath
            # Assert each element of sub_texts is a str
            gen_is_strs = (isinstance(sub_text, str) for sub_text in sub_texts)
            sub_text_and_type_pairs = tuple((sub_text,type(sub_text)) for sub_text in sub_texts)
            assert all(gen_is_strs), \
                (sub_text_and_type_pairs[:5], "And there is more. The following is the regex pattern", xpath)
            # Assert each element of sub_text is a str of length
            gen_is_str_length = (len(sub_text) > 0 for sub_text in sub_texts)
            sub_text_and_len = tuple((sub_text,len(sub_text)) for sub_text in sub_texts)
            assert all(gen_is_str_length), \
                (sub_text_and_len[:5], "And there is more. The following is the regex pattern", xpath)


class TestMain(unittest.TestCase):
    wishlist_path = TEST_ASSETS_FILES_WISHLISTS[0]

    def setUp(self) -> None:
        # Prevent print-out  # https://stackoverflow.com/a/63631661
        self.suppress_text = io.StringIO()
        sys.stdout = self.suppress_text 

    def tearDown(self) -> None:
        # Restoring print-out
        sys.stdout = sys.__stdout__

    def get_io_stream_text(self)->str:
        """ Returns text stored in diverted IOString. """
        return self.suppress_text.getvalue()

    def test_positive(self):
        """ Just run the 'main' function of 'CalculateTotal' and see if it works. """
        # Run the program with a built-in wishlist
        obj = lib.CalculateTotal(self.wishlist_path)
        obj.main()
        # Get the print-out at that point in testing
        print_out = self.get_io_stream_text()
        assert "This is how much it cost" in print_out, print_out
        assert print_out.count("This is how much it cost") > 1, print_out
        assert "This is how much shipping cost: $" in print_out, print_out


        # Run the program with breakdown read-out.
        obj2 = lib.CalculateTotal(self.wishlist_path, breakdown=True)
        obj2.main()
        # Get the print-out at that point in testing
        print_out2 = self.get_io_stream_text().replace(print_out, "")
        assert print_out not in print_out2
        # Function output assertions.
        assert "This is how much it cost" in print_out2, print_out2
        assert print_out2.count("This is how much it cost") > 1
        assert "This is how much shipping cost: $" in print_out2, print_out2
        # breakdown specific
        assert "Item cost: $" in print_out2, print_out2
        assert print_out2.count("Item cost: $") > 20
