import unittest

from etl.transform import clean_record
from ingest import build_documents


class TestCleanRecord(unittest.TestCase):
    def test_valid_record_is_cleaned(self):
        doc = clean_record(
            {"title": "  Hello ", "content": "Body", "published_date": "2026-1-2"}, "src"
        )
        self.assertEqual(doc["title"], "Hello")
        self.assertEqual(doc["published_date"], "2026-01-02")
        self.assertIsNone(doc["category"])

    def test_missing_title_raises(self):
        with self.assertRaises(ValueError):
            clean_record({"title": "  ", "content": "x"}, "src")

    def test_bad_date_raises(self):
        with self.assertRaises(ValueError):
            clean_record({"title": "T", "published_date": "01/02/2026"}, "src")


class TestBuildDocuments(unittest.TestCase):
    def test_duplicates_are_rejected(self):
        rec = {"title": "Same", "content": "Same"}
        docs, rejected = build_documents([rec, rec], "src")
        self.assertEqual(len(docs), 1)
        self.assertEqual(rejected, [(2, "duplicate")])


if __name__ == "__main__":
    unittest.main()