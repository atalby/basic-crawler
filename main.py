import json
from crawler.core import crawl

if __name__ == "__main__":
    start_url = "https://www.python.org"
    max_depth = 2

    results = crawl(start_url, depth=max_depth)

    output = {
        "start_url": start_url,
        "depth_limit": max_depth,
        "results": results
    }

    with open("crawl_result.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"\n[✅] Saved {len(results)} pages to crawl_result.json")

