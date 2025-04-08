import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urldefrag, urlparse
from typing import Set
from pathlib import Path

SKIP_EXTENSIONS = {
    ".png", ".jpg", ".jpeg", ".gif", ".svg", ".bmp", ".ico",
    ".pdf", ".xml", ".psd", ".zip", ".rar", ".7z", ".tar", ".gz", ".exe",
    ".dmg", ".iso", ".mp3", ".mp4", ".avi", ".mkv"
}

def should_skip_url(url: str) -> bool:
    return Path(urlparse(url).path).suffix.lower() in SKIP_EXTENSIONS


def crawl(url: str, visited: Set[str] = None, depth: int = 2, domain: str = None) -> list[dict]:
    if visited is None:
        visited = set()

    if domain is None:
        domain = urlparse(url).netloc

    if url in visited or depth < 0 or should_skip_url(url):
        return []

    parsed_url = urlparse(url)
    if parsed_url.netloc != domain:
        return []

    print(f"[CRAWL][depth={depth}] Visiting: {url}")
    visited.add(url)

    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
    except Exception as e:
        print(f"[ERROR] Failed to fetch {url}: {e}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')

    title = soup.title.string.strip() if soup.title else "(No title)"
    description_tag = soup.find("meta", attrs={"name": "description"})
    description = description_tag["content"].strip() if description_tag and description_tag.has_attr("content") else "(No description)"

    headings = [h.get_text(strip=True) for h in soup.find_all("h1")]

    results = [{
        "url": url,
        "title": title,
        "description": description,
        "headings": headings
    }]

    links = set()

    for tag in soup.find_all('a', href=True):
        raw_link = tag['href']
        absolute = urldefrag(urljoin(url, raw_link)).url
        if absolute not in visited:
            parsed = urlparse(absolute)
            if parsed.netloc == domain:
                links.add(absolute)

    for link in links:
        results.extend(crawl(link, visited, depth - 1, domain))

    return results

