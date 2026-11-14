"""Get real data from an API and a CSV, clean it, and save it."""
import requests
import pandas as pd

from ingest import build_documents

QUERY = "machine learning"  #Change to whatever


def get_hacker_news(query):
    """Ask the Hacker News API for stories. Returns a list of dictionaries."""
    response = requests.get(
        "https://hn.algolia.com/api/v1/search",
        params={"query": query, "tags": "story", "hitsPerPage": 100},
        timeout=30,
    )
    response.raise_for_status()  # stop with an error if the request failed
    hits = response.json()["hits"]

    records = []
    for hit in hits:
        records.append({
            "title": hit.get("title"),
            "content": hit.get("story_text") or "",
            "published_date": (hit.get("created_at") or "")[:10],  # keep YYYY-MM-DD
            "category": None,
            "url": hit.get("url"),
        })
    return records


def get_csv(path):
    """Read a CSV file with pandas. Returns a list of dictionaries."""
    df = pd.read_csv(path, dtype=str)  # read everything as text
    df = df.fillna("")                 # empty cells become "" instead of NaN
    return df.to_dict(orient="records")


def main():
    sources = [
        ("Hacker News", get_hacker_news(QUERY)),
        ("Sample CSV", get_csv("data/sample_documents.csv")),
    ]
    all_documents = []
    for name, raw_records in sources:
        documents, rejected = build_documents(raw_records, name)
        print(f"{name}: fetched {len(raw_records)}, kept {len(documents)}, rejected {len(rejected)}")
        all_documents.extend(documents)

    # Put everything in a pandas table.
    df = pd.DataFrame(all_documents)
    df = df.drop_duplicates(subset="content_hash")
    df = df.sort_values("published_date", ascending=False)

    print("\nDocuments per source:")
    print(df.groupby("source_name").size())

    df.to_csv("data/documents.csv", index=False)
    print(f"\nSaved {len(df)} documents to data/documents.csv")


if __name__ == "__main__":
    main()