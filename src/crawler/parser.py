from bs4 import BeautifulSoup
from crawler.models import PageData

def parse_html(url: str, html: str) -> PageData:
    soup = BeautifulSoup(html, "html.parser")
    title = soup.title.string.strip() if soup.title else None

    meta = soup.find("meta", attrs={"name": "description"})
    description = meta["content"].strip() if meta and "content" in meta.attrs else None

    headings = [h.get_text(strip=True) for h in soup.find_all("h1")]
    return PageData(url=url, title=title, description=description, headings=headings)

