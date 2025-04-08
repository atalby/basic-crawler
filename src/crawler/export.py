from crawler.models import PageData

def export_to_jsonl(pages: list[PageData], filepath: str) -> None:
    import json

    with open(filepath, "w", encoding="utf-8") as f:
        for page in pages:
            json.dump(vars(page), f, ensure_ascii=False)
            f.write("\n")

