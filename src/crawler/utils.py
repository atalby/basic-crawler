from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from pathlib import Path

SKIP_EXTENSIONS = {
    ".png", ".jpg", ".jpeg", ".gif", ".svg", ".bmp", ".ico",
    ".pdf", ".xml", ".psd", ".zip", ".rar", ".7z", ".tar", ".gz", ".exe",
    ".dmg", ".iso", ".mp3", ".mp4", ".avi", ".mkv"
}


def should_skip_url(url: str) -> bool:
    return Path(urlparse(url).path).suffix.lower() in SKIP_EXTENSIONS


def extract_metadata(html: str) -> tuple[str, str, list[str]]:
    soup = BeautifulSoup(html, "html.parser")
    title = soup.title.string.strip() if soup.title and soup.title.string else ""
    desc_tag = soup.find("meta", attrs={"name": "description"})
    description = desc_tag["content"].strip() if desc_tag and "content" in desc_tag.attrs else ""
    headings = [h.get_text(strip=True) for h in soup.find_all("h1")]
    return title, description, headings


def extract_links(html: str, base_url: str) -> list[str]:
    soup = BeautifulSoup(html, "html.parser")
    links = []
    for tag in soup.find_all("a", href=True):
        href = tag["href"]
        absolute_url = urljoin(base_url, href)
        links.append(absolute_url)
    return links

