"""Extract: read a file and return a list of dictionaries."""
import csv
import json
from pathlib import Path


def read_file(path):
    path = Path(path)

    if path.suffix == ".json":
        with open(path, encoding="utf-8") as file:
            data = json.load(file)
        if not isinstance(data, list):
            raise ValueError("JSON file must contain a list of records")
        return data

    if path.suffix == ".csv":
        with open(path, encoding="utf-8", newline="") as file:
            return list(csv.DictReader(file))

    raise ValueError(f"unsupported file type: {path.suffix}")