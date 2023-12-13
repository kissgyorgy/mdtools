from pathlib import Path

import click

from . import clean, fix
from .db_to_files import convert_table
from .diff import get_diff


@click.group()
def main():
    pass


@main.command()
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
def db2obsidian(database, table, body_column, single_val_column, bool_column):
    """Convert an SQLite database table to a set of Markdown files."""
    convert_table(database, table, body_column, single_val_column, bool_column)


@main.command("clean")
@click.argument("path", type=click.Path(exists=True, path_type=Path), nargs=-1)
def clean_file(path):
    """Clean up text from unwanted strings."""
    for p in path:
        if not p.is_file():
            continue
        click.echo(f"Cleaning {p}")
        content = p.read_text()
        word_diff = True

        cleaned = clean.remove_youtube_title(content)
        cleaned = clean.remove_link_from_title(cleaned)
        cleaned = clean.remove_empty_link_from_title_end(cleaned)
        cleaned, sub_count = clean.remove_newlines_from_code(cleaned)
        if sub_count != 0:
            word_diff = False

        cleaned, changed = fix.convert_quote_to_code(cleaned)
        if changed:
            word_diff = False

        diff, is_different = get_diff(p, cleaned, word_diff=word_diff)
        if not is_different:
            continue

        click.echo("Diff: " + diff)
        if click.confirm("Do you approve these changes?"):
            p.write_text(cleaned)
        else:
            click.echo(f"Skipping {p}")
