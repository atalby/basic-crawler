from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup

from crawler.utils import should_skip_url

def extract_links(soup: BeautifulSoup, base_url: str, domain: str, visited: set[str], allow_external: bool) -> set[str]:
    links = set()
    for tag in soup.find_all("a", href=True):
        raw = tag["href"]
        absolute = urljoin(base_url, raw)
        parsed = urlparse(absolute)

        if should_skip_url(absolute):
            continue

        if (allow_external or parsed.netloc == domain) and absolute not in visited:
            links.add(absolute)
    return links

