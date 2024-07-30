# Import Readwise Highlights into SQLite

Self-explanatory. Nice and simple importer for readwise highlights into a datasette (SQLite) db.

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

### Embeddings

```shell
llm embed-multi highlights \
  -d highlights.db \
  --sql 'SELECT
	  h.id as id,
    h.text AS highlight,
    b.title AS book_or_article_name,
    b.author AS author,
    h.highlighted_at AS date_highlight_was_made
FROM
    readwise_highlights h
JOIN
    readwise_books b ON h.book_id = b.id'
```

And then to search on the collection:

```shell
llm similar highlights -d highlights.db -c "food production"
```

Cool!

### Example Queries

Get highlight, book name, author, and highlight date in a single query:

```sql
SELECT
	  h.id as id,
    h.text AS highlight,
    b.title AS book_or_article_name,
    b.author AS author,
    h.highlighted_at AS date_highlight_was_made
FROM
    readwise_highlights h
JOIN
    readwise_books b ON h.book_id = b.id;
```