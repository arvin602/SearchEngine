"""Transform: clean and validate one record."""
import hashlib
from datetime import datetime


def clean_record(raw, source_name):
    """Return a clean dictionary, or raise ValueError if the record is bad."""
    title = (raw.get("title") or "").strip()
    if not title:
        raise ValueError("missing title")

    content = (raw.get("content") or "").strip()

    published_date = None
    raw_date = (raw.get("published_date") or "").strip()
    if raw_date:
        try:
            published_date = datetime.strptime(raw_date, "%Y-%m-%d").date().isoformat()
        except ValueError:
            raise ValueError(f"bad date: {raw_date!r}")

    category = (raw.get("category") or "").strip() or None
    url = (raw.get("url") or "").strip() or None

    # Same title + content always gives the same hash (used to spot duplicates).
    text = f"{title.lower()}|{content.lower()}"
    content_hash = hashlib.sha256(text.encode("utf-8")).hexdigest()

    return {
        "title": title,
        "content": content,
        "published_date": published_date,
        "source_name": source_name,
        "category": category,
        "url": url,
        "content_hash": content_hash,
    }