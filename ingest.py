"""Usage: python ingest.py data/sample_documents.json "Waterloo News API" """
import sys

from etl.extract import read_file
from etl.transform import clean_record


def build_documents(raw_records, source_name):
    """Return (documents, rejected). rejected is a list of (row_number, reason)."""
    documents = []
    rejected = []
    seen_hashes = set()

    for row_number, raw in enumerate(raw_records, start=1):
        try:
            doc = clean_record(raw, source_name)
        except ValueError as e:
            rejected.append((row_number, str(e)))
            continue

        if doc["content_hash"] in seen_hashes:
            rejected.append((row_number, "duplicate"))
            continue

        seen_hashes.add(doc["content_hash"])
        documents.append(doc)

    return documents, rejected


def main():
    if len(sys.argv) != 3:
        print('Usage: python ingest.py <file.json|file.csv> "<source name>"')
        sys.exit(1)
    path, source_name = sys.argv[1], sys.argv[2]

    try:
        raw_records = read_file(path)
    except (OSError, ValueError) as e:
        print(f"Could not read file: {e}")
        sys.exit(1)

    documents, rejected = build_documents(raw_records, source_name)

    print(f"Read {len(raw_records)} records")
    print(f"Valid: {len(documents)}  Rejected: {len(rejected)}")
    for row_number, reason in rejected:
        print(f"  row {row_number}: {reason}")

    if documents:
        print("\nFirst valid record:")
        print(documents[0])


if __name__ == "__main__":
    main()