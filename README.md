# Database to Markdown

This quick and dirty tool converts SQLite database tables to Obsidian Markdwon files.

It introspects the database table and converts the rows to properties in front matter.

The content of the Markdown file can be parametrized.

## Usage
```
Usage: db2obsidian [OPTIONS] DATABASE TABLE

Options:
  --body-column TEXT        This column will be the content of the Markdown
                            file. Can be specified multiple times, they will
                            be concatenated with newlines.
  --single-val-column TEXT  Convert a list to a single value (takes first
                            element).
  --bool-column TEXT        Converts an int column to a boolean value. Values
                            are not checked.
  --help                    Show this message and exit.
```

## Development

I'm not interested developing this tool myself, because it solved all my needs, but 
I accept Pull Requests if you want to improve it.
