from urllib.parse import urlparse
from collections import deque
from dataclasses import asdict

from crawler.export import export_results
from crawler.fetcher import fetch_html
from crawler.utils import extract_metadata, extract_links, should_skip_url
from crawler.storage import save_page
from crawler.types import PageData


def crawl(
    url: str,
    depth: int = 2,
    visited: set[str] = None,
    allow_external: bool = False
) -> list[PageData]:
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

    title, description, headings = extract_metadata(html)
    page_data = PageData(
        url=url,
        title=title,
        description=description,
        headings=headings
    )
    save_page(page_data)

    results = [page_data]
    if depth > 0:
        for link in extract_links(html, base_url=url):
            if should_skip_url(link):
                continue
            if not allow_external and urlparse(link).netloc != domain:
                continue
            results.extend(crawl(link, depth=depth - 1, visited=visited, allow_external=allow_external))

    return results


def crawl_and_export(url: str, depth: int = 2, export_format: str = "json", filename: str = "output.json"):
    results = crawl(url, depth=depth)
    export_results([asdict(page) for page in results], export_format, filename)

