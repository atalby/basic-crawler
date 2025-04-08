from pathlib import Path
from sqlite_utils import Database
from .models import PageData

db_path = Path(__file__).resolve().parent.parent / "data" / "crawler.db"
db_path.parent.mkdir(parents=True, exist_ok=True)
db = Database(db_path)

if "pages" not in db.table_names():
    db["pages"].create({
        "url": str,
        "title": str,
        "description": str,
        "headings": str
    }, pk="url")


def save_page(data: PageData):
    db["pages"].upsert({
        "url": data.url,
        "title": data.title,
        "description": data.description,
        "headings": "\n".join(data.headings)
    }, pk="url")

