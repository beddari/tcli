from pkg_resources import iter_entry_points

import click
from click_plugins import with_plugins


@with_plugins(iter_entry_points('tcli.plugins'))
@click.group()
def cli():
    """tcli is a modular command line tool wrapping and simplifying common
    team related tasks."""


@cli.group()
def christmas():
  """This is the christmas module."""


@christmas.command()
@click.option('--count', default=1, help='number of greetings')
@click.argument('name')
def greet(count, name):
    for x in range(count):
        click.echo('Merry christmas %s!' % name)
