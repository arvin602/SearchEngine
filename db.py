"""Everything that talks to PostgreSQL: connect and load documents."""
import os

import psycopg2
from dotenv import load_dotenv


def get_connection():
    load_dotenv()  # reads DATABASE_URL from your .env file
    url = os.environ.get("DATABASE_URL")
    if not url:
        raise RuntimeError("DATABASE_URL is not set (copy .env.example to .env)")
    # search_path lets us write "documents" instead of "search_engine.documents"
    return psycopg2.connect(url, options="-c search_path=search_engine")


def load_documents(conn, documents, source_types):
    """Insert cleaned documents. Safe to run twice: duplicates are skipped."""
    inserted = 0
    with conn.cursor() as cur:
        for doc in documents:
            # 1. make sure the source exists, then get its id
            cur.execute(
                "INSERT INTO sources (name, type) VALUES (%s, %s) "
                "ON CONFLICT (name) DO NOTHING",
                (doc["source_name"], source_types[doc["source_name"]]),
            )
            cur.execute("SELECT source_id FROM sources WHERE name = %s", (doc["source_name"],))
            source_id = cur.fetchone()[0]

            # 2. same for the category (if there is one)
            category_id = None
            if doc["category"]:
                cur.execute(
                    "INSERT INTO categories (name) VALUES (%s) ON CONFLICT (name) DO NOTHING",
                    (doc["category"],),
                )
                cur.execute("SELECT category_id FROM categories WHERE name = %s", (doc["category"],))
                category_id = cur.fetchone()[0]

            # 3. insert the document; a duplicate (same source + hash) is skipped
            cur.execute(
                "INSERT INTO documents "
                "(source_id, category_id, title, content, published_date, url, content_hash) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s) "
                "ON CONFLICT (source_id, content_hash) DO NOTHING",
                (source_id, category_id, doc["title"], doc["content"],
                 doc["published_date"], doc["url"], doc["content_hash"]),
            )
            inserted += cur.rowcount  # 1 if inserted, 0 if skipped
    return inserted