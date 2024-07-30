import os
import click
import sqlite_utils
import requests
import funcy_pipe as fp

READWISE_API_BASE_URL = "https://readwise.io/api/v2"


def fetch_from_books_api(token, params={}):
    all_books = []
    page = 1

    while True:
        params["page"] = page
        headers = {"Authorization": f"Token {token}"}
        response = requests.get(
            f"{READWISE_API_BASE_URL}/books/", headers=headers, params=params
        )
        response.raise_for_status()
        data = response.json()

        all_books.extend(data["results"])
        if data["next"] is None:
            break
        page += 1

    return all_books


# https://readwise.io/api_deets
def fetch_from_export_api(token, updated_after=None):
    full_data = []
    next_page_cursor = None

    while True:
        params = {}
        if next_page_cursor:
            params["pageCursor"] = next_page_cursor
        if updated_after:
            params["updatedAfter"] = updated_after

        # print("Making export api request with params " + str(params) + "...")

        response = requests.get(
            url=f"{READWISE_API_BASE_URL}/export/",
            params=params,
            headers={"Authorization": f"Token {token}"},
            verify=False,
        )
        full_data.extend(response.json()["results"])
        next_page_cursor = response.json().get("nextPageCursor")
        if not next_page_cursor:
            break

    return full_data


@click.command()
@click.option("--dbname", default="data.db", help="Name of the SQLite database file")
def main(dbname):
    token = os.environ["READWISE_API"]

    books = fetch_from_books_api(token)
    raw_highlights = fetch_from_export_api(token)

    highlight_sources = raw_highlights | fp.pmap(fp.omit("highlights")) | fp.to_list()
    highlights = raw_highlights | fp.pluck("highlights") | fp.flatten() | fp.to_list()

    db = sqlite_utils.Database(dbname)

    highlights_table = db.table("readwise_highlights", pk="id")
    highlights_table.upsert_all(highlights, alter=True)

    highlight_sources_table = db.table("readwise_highlight_sources", pk="user_book_id")
    highlight_sources_table.upsert_all(highlight_sources, alter=True)

    books_table = db.table("readwise_books", pk="id")
    books_table.upsert_all(books, alter=True)


if __name__ == "__main__":
    main()
