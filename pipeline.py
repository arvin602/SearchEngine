"""Run the whole pipeline: fetch -> clean -> load into PostgreSQL.

Usage:
    python pipeline.py              (searches for QUERY from fetch_data.py)
    python pipeline.py "my topic"   (searches for your own topic)

It is safe to run again and again: documents already in the database are skipped.
"""
import sys

from db import get_connection, load_documents
from fetch_data import QUERY, get_csv, get_hacker_news
from ingest import build_documents


def run(query):
    # (source name, source type, raw records from that source)
    sources = [
        ("Hacker News", "api", get_hacker_news(query)),
        ("Sample CSV", "csv", get_csv("data/sample_documents.csv")),
    ]

    # Clean each source with the Week 3 code, then pile everything together.
    all_documents = []
    source_types = {}
    for name, source_type, raw_records in sources:
        documents, rejected = build_documents(raw_records, name)
        print(f"{name}: fetched {len(raw_records)}, valid {len(documents)}, rejected {len(rejected)}")
        all_documents.extend(documents)
        source_types[name] = source_type

    # Load into PostgreSQL. "with conn" saves everything if it works,
    # and undoes everything if there is an error.
    conn = get_connection()
    with conn:
        inserted = load_documents(conn, all_documents, source_types)
    conn.close()

    print(f"Loaded {inserted} new documents ({len(all_documents) - inserted} already existed)")


if __name__ == "__main__":
    run(sys.argv[1] if len(sys.argv) > 1 else QUERY)