import contextlib
import sqlite3
import textwrap
from pathlib import Path

import yaml


def convert_table(
    database_file,
    table_name,
    body_columns,
    single_val_columns,
    bool_columns=None,
    output_dir=None,
    name_column="name",
):
    if output_dir is None:
        output_dir = table_name
    if bool_columns is None:
        bool_columns = []

    with connect_db(database_file) as cursor:
        columns = get_columns(table_name, cursor)
        rows = get_rows(table_name, cursor)

    outdir = Path(output_dir)
    outdir.mkdir()

    for row in rows:
        filename = outdir / f"{row[name_column]}.md"
        filename.parent.mkdir(exist_ok=True)
        create_md(
            columns, body_columns, single_val_columns, bool_columns, row, filename
        )


@contextlib.contextmanager
def connect_db(database_file):
    connection = sqlite3.connect(database_file)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    yield cursor
    cursor.close()
    connection.close()


def get_columns(table_name, cursor):
    # Retrieve the column names from the table
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = [row[1] for row in cursor.fetchall()]
    return columns


def get_rows(table_name, cursor):
    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()
    return rows


def create_md(columns, body_columns, single_val_columns, bool_columns, row, filename):
    exclude_columns = {*body_columns, "id"}

    yaml_data = dict()
    for column, value in zip(columns, row):
        if column in exclude_columns:
            continue
        value = bool(value) if column in bool_columns else value
        # breakpoint()
        value = convert_list(value, single_val=column in single_val_columns)
        yaml_data[column] = value

    with open(filename, "w") as md_file:
        md_file.write("---\n")
        yaml.dump(yaml_data, md_file, allow_unicode=True, default_flow_style=False)
        md_file.write("---\n\n")
        body_parts = []
        for body_col in body_columns:
            part = textwrap.fill(row[body_col], width=88, break_long_words=False)
            body_parts.append(part)
        md_file.write("\n".join(body_parts) + "\n")


def convert_list(value, *, single_val):
    if not isinstance(value, str) or not value.startswith("["):
        return value

    no_brackets = value[1:-1]
    no_quotes = no_brackets.replace('"', "")
    no_space_between_separator = no_quotes.replace(", ", ",")
    converted_list = no_space_between_separator.split(",")
    if not all(converted_list):
        return []
    elif single_val:
        return converted_list[0]
    else:
        return converted_list
