import click

import lib

@click.group()
def cli():
    pass

@cli.command()
@click.option('-p', '--path', type=str, default=lib.CalculateTotal.wishlist_path)
@click.option('-v', '--verbose', count=True)
def main(path, verbose):
    # Introduction
    click.echo("Hello World.")

    # Set logging level
    logging_level = lib.dict_log_level[verbose]
    lib.logging.getLogger().setLevel(logging_level)
    lib.logging.info("Meh")

    # Run main function
    calc_obj = lib.CalculateTotal(wishlist_path=path)
    calc_obj.main()

@cli.command()
@click.argument('patt', type=str)
@click.option('--limit', type=int, default=lib.CLI_REGEX_FIND_LIMIT)
def regex_find(patt, limit):
    calc_obj = lib.CalculateTotal()
    calc_obj.list_regex_matches(patt, limit)


if __name__ == "__main__":
    cli()