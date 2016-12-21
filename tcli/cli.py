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


import tcli.utils
from subprocess import call


def add_exec_plugin(name, cmd):
    @cli.command(name=name, context_settings=dict(
        ignore_unknown_options=True,
    ))
    @click.argument('cmd_args', nargs=-1, type=click.UNPROCESSED)
    def exec_plugin(cmd_args):
        """A tcli exec plugin."""
        cmdline = [cmd] + list(cmd_args)
        call(cmdline)


FILTER="^%s-(.*)$" % __package__
for name, cmd in tcli.utils.find_plugin_executables(FILTER):
    add_exec_plugin(name, cmd)
