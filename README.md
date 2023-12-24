# Import Readwise Highlights into SQLite

Self-explanatory. Nice and simple importer for datasette.

```shell
pip install readwise-to-datasette
readwise-to-datasette
```

Or, from source:

```python
poetry install
poetry run readwise-to-datasette
```

## Getting an API Key

Find it here: <https://readwise.io/access_token>

## Exploring the data

```shell
pip install datasette
datasette serve data.db
```