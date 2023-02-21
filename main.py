import click

import lib

@click.group()
def cli():
    pass

@click.group()
def examples():
    pass
cli.add_command(examples)

@cli.command()
@click.option('-p', '--path', type=str, default=lib.CalculateTotal.wishlist_path)
@click.option('-v', '--verbose', count=True)
@click.option('-b', '--breakdown', is_flag=True, default=False)
def main(path, verbose, breakdown):
    # Introduction
    click.echo("Hello World.")
    # Set logging level
    logging_level = lib.dict_log_level[verbose]
    lib.logging.getLogger().setLevel(logging_level)
    lib.logging.info("Meh")
    # Run main function
    calc_obj = lib.CalculateTotal(wishlist_path=path, breakdown=breakdown)
    calc_obj.main()

@cli.command()
@click.argument('patt', type=str)
@click.option('--limit', type=int, default=lib.CLI_REGEX_FIND_LIMIT)
def regex_find(patt, limit):
    calc_obj = lib.CalculateTotal()
    calc_obj.list_regex_matches(patt, limit)

@cli.command()
@click.argument('xpath', type=str)
@click.option('--limit', type=int, default=lib.CLI_XPATH_FIND_LIMIT)
def xpath_find(xpath, limit):
    calc_obj = lib.CalculateTotal()
    calc_obj.list_xpath_matches(xpath, limit)


@examples.command()
@click.option('-b', '--breakdown', is_flag=True, default=False)
def main(breakdown):
    # Introduction
    click.echo("Example of main.")
    # Run main function
    calc_obj = lib.CalculateTotal(wishlist_path=lib.TEST_ASSETS_FILES_WISHLISTS[1], breakdown=breakdown)
    calc_obj.main()

@examples.command()
@click.option('-o', '--option', type=int, default=0)
def xpath_find(option):
    if option == 0:
        calc_obj = lib.CalculateTotal()
        calc_obj.list_xpath_matches(lib.XPATH_PRICE)
    elif option == 1:
        calc_obj = lib.CalculateTotal(wishlist_path=lib.TEST_ASSETS_FILES_WISHLISTS[1])
        calc_obj.list_xpath_matches(lib.XPATH_SHIPPING_PRICE)


if __name__ == "__main__":
    cli()