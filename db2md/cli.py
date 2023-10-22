import click

from .convert import convert_table_to_yaml


@click.command
@click.argument("database")
@click.argument("table")
@click.option("--body-column", multiple=True)
@click.option("--single-val-column", multiple=True)
@click.option("--bool-column", multiple=True)
def main(database, table, body_column, single_val_column, bool_column):
    convert_table_to_yaml(database, table, body_column, single_val_column, bool_column)
