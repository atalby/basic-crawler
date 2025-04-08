from sqlite_utils import Database
import json
import csv

def export_results(data: list[dict], format: str, output_path: str = None):
    if format == "json":
        with open(output_path or "out.json", "w") as f:
            json.dump(data, f, indent=2)
    elif format == "jsonl":
        with open(output_path or "out.jsonl", "w") as f:
            for entry in data:
                f.write(json.dumps(entry) + "\n")
    elif format == "csv":
        with open(output_path or "out.csv", "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["url", "title", "description", "headings"])
            writer.writeheader()
            for entry in data:
                writer.writerow(entry)
    else:
        raise ValueError(f"Unsupported format: {format}")

def export_from_db(format: str, db_path: str = "src/data/crawler.db"):
    db = Database(db_path)
    if "pages" not in db.table_names():
        raise RuntimeError("No pages table found in database.")

    rows = list(db["pages"].rows)
    for row in rows:
        if isinstance(row.get("headings"), str):
            try:
                row["headings"] = json.loads(row["headings"])
            except Exception:
                pass
    export_results(rows, format)

