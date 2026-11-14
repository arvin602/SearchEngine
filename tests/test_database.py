"""Database tests. They are skipped automatically if PostgreSQL isn't reachable."""
import unittest

from db import get_connection, load_documents
from ingest import build_documents


def database_available():
    try:
        get_connection().close()
        return True
    except Exception:
        return False


@unittest.skipUnless(database_available(), "database not available")
class TestLoad(unittest.TestCase):
    def setUp(self):
        self.conn = get_connection()
        raw = [
            {"title": "First", "content": "one", "published_date": "2026-01-01", "category": "Tech"},
            {"title": "Second", "content": "two", "published_date": "2026-01-02"},
        ]
        self.docs, _ = build_documents(raw, "Test Source")
        self.types = {"Test Source": "api"}

    def tearDown(self):
        self.conn.rollback()  # undo everything the test did
        self.conn.close()

    def test_documents_are_loaded(self):
        self.assertEqual(load_documents(self.conn, self.docs, self.types), 2)
        with self.conn.cursor() as cur:
            cur.execute("SELECT count(*) FROM documents WHERE title IN ('First', 'Second')")
            self.assertEqual(cur.fetchone()[0], 2)

    def test_load_twice_does_not_duplicate(self):
        load_documents(self.conn, self.docs, self.types)
        self.assertEqual(load_documents(self.conn, self.docs, self.types), 0)


if __name__ == "__main__":
    unittest.main()