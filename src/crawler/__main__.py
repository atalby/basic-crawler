import argparse
from crawler.core import crawl

def main():
    parser = argparse.ArgumentParser(description="Basic Web Crawler")
    parser.add_argument("url", help="Starting URL")
    parser.add_argument("--depth", type=int, default=2, help="Depth limit for crawling")
    parser.add_argument("--allow-external", action="store_true", help="Allow crawling external domains")
    args = parser.parse_args()

    results = crawl(
        url=args.url,
        depth=args.depth,
        allow_external=args.allow_external
    )

    for page in results:
        print(f"URL: {page.url}")
        print(f"Title: {page.title}")
        print(f"Description: {page.description}")
        print(f"Headings: {page.headings}")
        print("-" * 80)

if __name__ == "__main__":
    main()

