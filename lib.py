import os
from pathlib import Path
from dataclasses import dataclass
import re
import glob

from lxml import etree

from PARAMS import *
import config


import logging
logging.basicConfig(format='%(asctime)s %(message)s', level=logging.WARNING)

dict_log_level = {
    0:logging.WARNING,
    1:logging.INFO,
    2:logging.DEBUG,
}


def file_exists(path:str, quiet=False) -> bool:
    """ 
    Confirms whether or not a file exists.
    If any error raise while quiet is true, return False, else escalate error.
    """
    try:
        return Path(path).is_file()
    except Exception as exc:
        if quiet:
            return False
        else:
            raise exc from None
        
def absolute_path(path:str)->str:
    """ Ensures path is absolute (from root of the computer system) """
    if os.path.isabs(path):
        return path
    else:
        return Path(path).absolute().__str__()
        
def _path_valid_absolute(path:str, quiet=False) -> 'str|None':
    """ 
    Returns a valid absolute path else 'None'.
    quiet: If any error raises, return None, else escalate error.
    """
    try:
        if file_exists(path):
            return Path(path).absolute()
        else:
            None
    except Exception as exc:
        if quiet:
            return None
        else:
            raise exc from None
        
def get_file_text(path:str, encoding="utf8", line_joiner:str="\n"):
    """ 
    Get text from file. 
    path: path to file. Must be valid.
    line_joiner: substitute character[s] for nextline
    """
    assert isinstance(path, str), path
    with open(path, encoding=encoding) as file:
        doc = file.readlines()
        text = line_joiner.join(doc)
        return text
    
def valid_wishlist_text(text:str) -> bool:
    """ 
    Validates whether text has html structure for finding wishlist.
    NB: Do note that this formula may need to change in order to facilitate
        any changes to the html structure Amazon may make to their website.
    """
    for patt in REGEX_VALID_WISHLIST_LIST:
        match_obj = re.search(patt, text)
        if match_obj is None:
            logging.debug("Bad regex pattern '{}' for text '{}'...".format(patt, text[:100]))
            break
    else:
        return True
    
def valid_wishlist_path(path:str) -> bool:
    """ 
    Validates whether text of a file of 'path' has html structure for finding wishlist.
    """
    text = get_file_text(path)
    return valid_wishlist_text(text)

def get_wishlist_files_in_directory(_test:bool=False)->'None|list[str]':
    """ 
    Get all html wishlist files in directory.
    Gets files according to file extension (*.htm[l])
    """
    paths = list()
    paths1 = glob.glob(GLOB_WISHLIST1, root_dir=os.getcwd(), recursive=True)
    paths2 = glob.glob(GLOB_WISHLIST2, root_dir=os.getcwd(), recursive=True)
    if _test:
        paths3 = glob.glob(GLOB_WISHLIST3, root_dir=os.getcwd(), recursive=True)
        paths4 = glob.glob(GLOB_WISHLIST4, root_dir=os.getcwd(), recursive=True)
    else:
        paths3, paths4 = list(), list()
    paths = paths1 + paths2 + paths3 + paths4
    return paths

def get_xpath_in_text(xpath:str, text:str)->list[str]:
    """
    Returns a list of xpath matches of text.
    """
    if not isinstance(xpath, str): raise TypeError("Argument 'xpath' '{}' is not of type 'str'.".format(xpath))
    if not isinstance(text, str): raise TypeError("Argument 'text' '{}' is not of type 'str'.".format(text))
    tree = etree.HTML(text)
    html_elements = tree.xpath(xpath)
    match_texts = list((ele.text for ele in html_elements))
    return match_texts


@dataclass
class CalculateTotal():
    wishlist_path : str = ""
    breakdown : bool = False

    def __post_init__(self):
        self.update_wishlist_file_path()

    def get_wishlist_file_path(self) -> str:
        """ 
        Get amazon wishlist file path.
        """
        max_test_points = 10     # Ensure it's higher than the amount of if-elif-else options
        for test_point in range(max_test_points):
            # Check user input/class
            if test_point == 0:
                path = self.wishlist_path
                if path:
                    logging.debug("Taking path '{}' from the class.".format(path))
                    path = absolute_path(path)
                    if file_exists(path, quiet=True):
                        if valid_wishlist_path(path):
                            return path
                        else:
                            logging.debug("File '{}' does not have a valid wishlist.".format(path))
                    else:
                        logging.debug("File '{}' does not exists.".format(path))
            # Check environment variables
            elif test_point == 1:
                path = os.environ.get(WISHLIST_PATH_ENV_NAME)
                if isinstance(path, str):
                    logging.debug("Taking path '{}' from the environment variables.".format(path))
                    path = absolute_path(os.environ.get(WISHLIST_PATH_ENV_NAME))
                    if file_exists(path, quiet=True):
                        if valid_wishlist_path(path):
                            return os.environ.get(WISHLIST_PATH_ENV_NAME)
                        else:
                            logging.debug("File '{}' does not have a valid wishlist.".format(path))
                    else:
                        logging.debug("File '{}' does not exists.".format(path))
            # Check config file
            elif test_point == 2:
                path = config.wishlist_path
                if isinstance(path, str) and bool(path):
                    logging.debug("Taking path '{}' from the config file.".format(path))
                    path = absolute_path(config.wishlist_path)
                    if file_exists(path, quiet=True):
                        if valid_wishlist_path(path):
                            return config.wishlist_path
                        else:
                            logging.debug("File '{}' does not have a valid wishlist.".format(path))
                    else:
                        logging.debug("File '{}' does not exists.".format(path))
            # Check root directory
            elif test_point == 3:
                paths = get_wishlist_files_in_directory()
                if len(paths) > 0:
                    logging.debug("Taking path '{}' from the config file.".format(path))
                    return paths[0]
            else:
                logging.error(ERROR_MSG_NO_WISHLIST)
                raise ValueError(ERROR_MSG_NO_WISHLIST)
        
    def update_wishlist_file_path(self) -> None:
        """ Sets the amazon wishlist file path in class """
        self.wishlist_path = self.get_wishlist_file_path()

    def wishlist_regex_matches(self, patt:str)->list[str]:
        """ 
        Sequence of regular expression matches found in wishlist.
        """
        text = get_file_text(self.wishlist_path)
        regex_matches = re.finditer(patt, text)
        # Extract text from each re match
        sub_texts = list((match.group(0) for match in regex_matches))
        return sub_texts

    def list_regex_matches(self, patt:str, limit=None):
        """ 
        Prints the regular expression matches found.
        limit: int representing maximum of printable values. abs(limit)
        """
        sub_texts = self.wishlist_regex_matches(patt)
        # Set a default max value for limit if none is given.
        limit = abs(limit) if isinstance(limit, int) else len(sub_texts)
        # OUTPUT text
        print("This is the pattern: {}".format(patt))
        for i, sub_text in enumerate(sub_texts):
            if i > limit:
                break
            print("{}. {}".format(i+1, sub_text))

    def wishlist_xpath_matches(self, xpath:str)->list[str]:
        """ 
        Sequence of xpath matches found in HTML wishlist.
        """
        wishlist_html_text = get_file_text(self.wishlist_path)
        sub_texts = get_xpath_in_text(xpath, wishlist_html_text)
        return sub_texts

    def list_xpath_matches(self, xpath:str, limit=None):
        """ 
        Print the xpath matches found.
        limit: int representing maximum of printable values. abs(limit)
        """
        sub_texts = self.wishlist_xpath_matches(xpath)
        # Set a default max value for limit if none is given.
        limit = abs(limit) if isinstance(limit, int) else len(sub_texts)
        # OUTPUT Text
        print("This is the xpath pattern: {}".format(xpath))
        for i, price in enumerate(sub_texts):
            print("{}. {}".format(i+1, price))


    def main(self)-> None:
        """ 
        Main function for reading and returning sum of items in amazon wishlist.
        """
        text = get_file_text(self.wishlist_path)
        
        # Method 1
        print("First search/parse method.")
        whole_num_cash = get_xpath_in_text(XPATH_WHOLE_PRICE, text)
        fraction_num_cash = get_xpath_in_text(XPATH_FRACTION_PRICE, text)
        moneys = list()
        for whole_text, fraction_text in zip(whole_num_cash, fraction_num_cash):
            cost_text = "{}.{}".format(whole_text.strip(), fraction_text.strip())
            cost = float(cost_text)
            moneys.append(cost)
            if self.breakdown: print("Item cost: ${:.2f}".format(cost))
        n_moneys = len(moneys)
        total = sum(moneys)
        print("Number of items: {}".format(n_moneys))
        print("This is how much it cost: ${:.2f}".format(total))

        # Method 2
        print("Second search/parse method.")
        cost_texts = get_xpath_in_text(XPATH_PRICE, text)
        moneys2 = list()
        for cost_text in cost_texts:
            # Remove money sign
            money_text = cost_text.strip().removeprefix('$').strip()
            cost = float(money_text)
            moneys2.append(cost)
            if self.breakdown: print("Item cost: ${:.2f}".format(cost))
        n_moneys2 = len(moneys2)
        total2 = sum(moneys2)
        print("Number of items: {}".format(n_moneys2))
        print("This is how much it cost: ${:.2f}".format(total2))

        #  Shipping Costs
        shipping_cost_texts = get_xpath_in_text(XPATH_SHIPPING_PRICE, text)
        moneys_shipping = list()
        for shipping_cost_text in shipping_cost_texts:
            # Get only number text
            money_match = re.search(REGEX_MONEY_NUMBER, shipping_cost_text)
            if money_match:
                cost = float(money_match.group(0))
                moneys_shipping.append(cost)
                if self.breakdown: print("Shipping cost: ${:.2f}".format(cost))
            else:
                logging.info("Shipping costs not found.")
        else:
            n_moneys_shipping = len(moneys_shipping)
            total_shipping = sum(moneys_shipping)
            print("Number of items with shipping cost: {}".format(n_moneys_shipping))
            print("This is how much shipping cost: ${:.2f}".format(total_shipping))
