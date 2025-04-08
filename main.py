import sys
import json
import argparse

sys.path.insert(0, "./src")

from crawler.core import crawl
from crawler.export import export_to_jsonl


def parse_args():
    parser = argparse.ArgumentParser(description="Basic Web Crawler")
    parser.add_argument("--url", type=str, required=True, help="Starting URL to crawl")
    parser.add_argument("--depth", type=int, default=2, help="Depth to crawl")
    parser.add_argument("--output", type=str, default="crawl_result.json", help="Output file name (JSON)")
    parser.add_argument("--format", type=str, default="json", choices=["json", "jsonl", "csv"],
                        help="Output format: json (default) or jsonl")
    parser.add_argument(
        "--allow-external",
        action="store_true",
        help="Allow crawling external domains (default is same-domain only)"
    )

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    results = crawl(args.url, depth=args.depth, allow_external=args.allow_external)
 
    if args.format == "jsonl":
        export_to_jsonl(results, args.output)
    else:
        output = {
            "start_url": args.url,
            "depth_limit": args.depth,
            "results": [vars(page) for page in results]
        }
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(output, f, ensure_ascii=False, indent=2)


    print(f"\n[✅] Saved {len(results)} pages to {args.output}")

