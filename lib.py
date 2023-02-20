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
        
def get_file_text(path, encoding="utf8", line_joiner:str="\n"):
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

# def get_wishlist_files_in_directory(directory:str=".", quiet=False)->'None|list[str]':
def get_wishlist_files_in_directory(_test=False)->'None|list[str]':
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


@dataclass
class CalculateTotal():
    wishlist_path : str = ""

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

    def list_regex_matches(self, patt=REGEX_COST, limit=None):
        """ 
        Prints the regular expression matches found.
        limit: int representing maximum of printable values. abs(limit)
        TODO: Remove default for patt
        """
        text = get_file_text(self.wishlist_path)
        sub_texts = re.findall(patt, text)
        limit = abs(limit) if isinstance(limit, int) else len(sub_texts)

        print("This is the pattern: {}".format(patt))
        for i, sub_text in enumerate(sub_texts):
            if i > limit:
                break
            print("{}. {}".format(i+1, sub_text))

    def list_xpath_matches(self, xpath=XPATH_PRICE, limit=None):
        """ 
        Print the xpath matches found.
        limit: int representing maximum of printable values. abs(limit)
        TODO: Remove default for xpath
        """
        text = get_file_text(self.wishlist_path)
        tree = etree.HTML(text)
        prices = tree.xpath(xpath)
        limit = abs(limit) if isinstance(limit, int) else len(prices)
        print("This is the xpath pattern: {}".format(xpath))
        for i, price in enumerate(prices):
            print("{}. {}".format(i+1, price))


    def main(self)-> None:
        """ Main function for reading and returning sum of items in amazon wishlist. """
        text = get_file_text(self.wishlist_path)
        tree = etree.HTML(text)
        whole_num_cash = tree.xpath(XPATH_WHOLE_PRICE)
        fraction_num_cash = tree.xpath(XPATH_FRACTION_PRICE)
        moneys = list()
        for ele_pair in zip(whole_num_cash, fraction_num_cash):
            cost_text = ".".join(ele.text.strip() for ele in ele_pair)
            cost = float(cost_text)
            moneys.append(cost)
        _sum = sum(moneys)
        print("This is how much it cost: ${:.2f}".format(_sum))