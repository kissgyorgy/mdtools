import click

from .convert import convert_table


@click.command
@click.argument("database")
@click.argument("table")
@click.option(
    "--body-column",
    multiple=True,
    help="This column will be the content of the Markdown file."
    " Can be specified multiple times,"
    " they will be concatenated with newlines.",
)
@click.option(
    "--single-val-column",
    multiple=True,
    help="Convert a list to a single value (takes first element).",
)
@click.option(
    "--bool-column",
    multiple=True,
    help="Converts an int column to a boolean value. Values are not checked.",
)
def main(database, table, body_column, single_val_column, bool_column):
    convert_table(database, table, body_column, single_val_column, bool_column)
