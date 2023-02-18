import click

import lib

@click.command()
def main():
    click.echo("Hello World.")
    lib.calc_total()

if __name__ == "__main__":
    main()