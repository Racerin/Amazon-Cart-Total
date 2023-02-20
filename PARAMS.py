WISHLIST_PATH_ENV_NAME = "AMAZON_WISHLIST_PATH"

XPATH_WHOLE_PRICE = r"//span[@class='a-price-whole']"
XPATH_FRACTION_PRICE = r"//span[@class='a-price-fraction']"
XPATH_CURRENCY = None
XPATH_PRICE = r"//span[@id='itemPrice_*']/span[@class='a-offscreen']"

REGEX_WHOLE_PRICE = r'class="a-price-whole">'
# REGEX_FRACTION_PRICE = XPATH_FRACTION_PRICE
# REGEX_CURRENCY = XPATH_CURRENCY
# REGEX_VALID_WISHLIST_LIST = (REGEX_WHOLE_PRICE, )
REGEX_VALID_WISHLIST_LIST = (REGEX_WHOLE_PRICE,)
REGEX_COST = r'(?>class="a-offscreen">\$)(\d+\.\d+)|(\d+)'

# GLOB_WISHLIST = "*\.htm?(l)"
# GLOB_WISHLIST = r"*.htm?(l)"
GLOB_WISHLIST1 = r"**[.]html"
GLOB_WISHLIST2 = r"**[.]htm"
GLOB_WISHLIST3 = r"**/*[.]htm"
GLOB_WISHLIST4 = r"**/*[.]htm"

CLI_REGEX_FIND_LIMIT = 1e3

TEST_ASSETS_FILES_WISHLISTS = (
    r'test\assets\wishlist1.html',
    r'test\assets\wishlist2.htm',
)

FILES_EXISTS = (
    'config.py',
    'lib.py',
    'main.py',
    'LICENSE',
    'PARAMS.py',
    'README.md',
    r'test/__init__.py',
    r'test/test_functions.py',
    *TEST_ASSETS_FILES_WISHLISTS,
)

DIRECTORIES = (
    '.',
    r'\test',
)

ERROR_MSG_NO_WISHLIST = "Failed to find a path for the wishlist. \
Please set the path of the wishlist within the config.py file, \
local environment variable (.env file or global). \
Also check that the file exist's at the described path/directory and is named accordingly \
OR is at the program directory."