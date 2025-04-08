# 🕷️ Basic Crawler

A simple and modular Python web crawler built with `requests` and `BeautifulSoup`. It recursively visits web pages starting from a root URL, collects structured metadata (title, description, headings), and exports the results to CSV, JSON, or JSONL formats.

---

## 🚀 Features

- Crawl any website recursively with configurable depth
- Skip non-HTML content automatically
- Optional restriction to the same domain
- Gracefully handles broken or slow links
- Exports data to:
  - `CSV`
  - `JSON`
  - `JSONL`
- Fully tested with `pytest`
- Modular design (clean separation of concerns)

---

## 🏗️ Project Structure

```
basic-crawler/
├── crawler/
│   ├── core.py             # Crawl logic
│   ├── fetcher.py          # HTTP requests
│   ├── parser.py           # HTML parsing
│   └── export.py           # Data exporting
├── tests/
│   └── test_core.py        # Pytest test cases
├── main.py                 # CLI entry point
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation

```bash
git clone https://github.com/atalby/basic-crawler.git
cd basic-crawler
python3 -m venv crawler-env
source crawler-env/bin/activate
pip install -r requirements.txt
```

---

## 🧪 Running Tests

```bash
pytest
```

All tests are located in the `tests/` directory.

---

## 🕹️ Usage

```bash
python main.py --url <START_URL> --depth <DEPTH> --format <json|jsonl|csv> --output <FILE>
```

### Example:

```bash
python main.py --url https://www.python.org --depth 1 --format jsonl --output out.jsonl
```

This will crawl up to 1 level deep from `https://www.python.org` and save results in JSONL format to `out.jsonl`.

---

## 📦 Output Example (JSON)

```json
{
  "url": "https://www.python.org",
  "title": "Welcome to Python.org",
  "description": "The official home of the Python Programming Language",
  "headings": ["Welcome", "Another Heading"]
}
```

---

## 🔧 Configuration Options

| Argument     | Description                            | Required | Default     |
|--------------|----------------------------------------|----------|-------------|
| `--url`      | Root URL to start crawling from         | ✅       | —           |
| `--depth`    | How deep to crawl (0 = just root)       | ❌       | `1`         |
| `--format`   | Output format (`json`, `jsonl`, `csv`)  | ❌       | `json`      |
| `--output`   | Output filename                         | ❌       | `output.json` |

---

## 🧠 Design Philosophy

This crawler is designed to be:
- **Simple**: Focused on clarity and correctness.
- **Extensible**: Easy to plug in additional parsers or filters.
- **Testable**: Built with test coverage in mind.

---

## 🪪 License

MIT License

---

## 👤 Author

**Anass Talby** — [LinkedIn](https://www.linkedin.com/in/anass-talby)

---

## 📬 Contributions

PRs are welcome! Please include tests for any new features.
