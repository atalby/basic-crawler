from urllib.parse import urlparse
from crawler.models import PageData
from crawler.fetcher import fetch_html
from crawler.parser import parse_html
from crawler.links import extract_links
from crawler.utils import should_skip_url
from bs4 import BeautifulSoup

def crawl(url: str, depth: int = 2, visited: set[str] = None, allow_external: bool = False) -> list[PageData]:
    if visited is None:
        visited = set()

    domain = urlparse(url).netloc
    if url in visited or depth < 0 or should_skip_url(url):
        return []

    visited.add(url)
    print(f"[CRAWL][depth={depth}] Visiting: {url}")

    html = fetch_html(url)
    if not html:
        return []

    soup = BeautifulSoup(html, "html.parser")
    result = parse_html(url, html)
    results = [result]

    links = extract_links(soup, url, domain, visited, allow_external=allow_external)
    for link in links:
        results.extend(crawl(link, depth=depth - 1, visited=visited, allow_external=allow_external))

    return results

