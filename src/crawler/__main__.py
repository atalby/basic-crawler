import argparse
from dataclasses import asdict
from crawler.core import crawl
from crawler.export import export_results

def main():
    parser = argparse.ArgumentParser(description="Basic web crawler")
    parser.add_argument("url", help="The starting URL to crawl")
    parser.add_argument("--depth", type=int, default=2, help="Maximum crawl depth")
    parser.add_argument("--allow-external", action="store_true", help="Allow crawling external domains")
    parser.add_argument("--export", choices=["json", "jsonl", "csv"], help="Export format")

    args = parser.parse_args()

    results = crawl(args.url, depth=args.depth, allow_external=args.allow_external)
    print(f"[DONE] Crawled {len(results)} pages.")

    if args.export:
        export_results([asdict(r) for r in results], args.export)

if __name__ == "__main__":
    main()

