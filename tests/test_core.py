import sys
import os
sys.path.insert(0, "./src")

from crawler.core import crawl_and_export
from crawler.core import crawl
from crawler.utils import should_skip_url
import requests
import json
from unittest.mock import patch, Mock

def test_should_skip_url():
    assert should_skip_url("https://example.com/image.png")
    assert should_skip_url("https://example.com/video.mp4")
    assert not should_skip_url("https://example.com/page")
    assert not should_skip_url("https://example.com/index.html")


@patch("crawler.fetcher.requests.get")
def test_basic_html_parsing(mock_get):
    html = """
    <html>
      <head>
        <title>Test Page</title>
        <meta name="description" content="This is a test page for the crawler.">
      </head>
      <body>
        <h1>Welcome</h1>
        <h1>Another Heading</h1>
        <a href="https://example.com/page2">Next</a>
      </body>
    </html>
    """
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.text = html
    mock_get.return_value = mock_response

    results = crawl("https://example.com", depth=0)

    assert len(results) == 1
    result = results[0]
    assert result.url == "https://example.com"
    assert result.title == "Test Page"
    assert result.description == "This is a test page for the crawler."
    assert result.headings == ["Welcome", "Another Heading"]

@patch("crawler.fetcher.requests.get")
def test_respects_depth_limit(mock_get):
    html = """
    <html>
      <head>
        <title>Root</title>
        <meta name="description" content="Root page">
      </head>
      <body>
        <h1>Top</h1>
        <a href="https://example.com/next">Next</a>
      </body>
    </html>
    """
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.text = html
    mock_get.return_value = mock_response

    results = crawl("https://example.com", depth=0)

    assert len(results) == 1
    assert results[0].url == "https://example.com"

@patch("crawler.fetcher.requests.get")
def test_respects_domain_restriction(mock_get):
    html = """
    <html>
      <head><title>Domain Test</title></head>
      <body>
        <h1>Main</h1>
        <a href="https://example.com/internal">Internal</a>
        <a href="https://other.com/external">External</a>
      </body>
    </html>
    """
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.text = html
    mock_get.return_value = mock_response

    results = crawl("https://example.com", depth=1)

    urls = {page.url for page in results}
    assert "https://example.com" in urls
    assert "https://example.com/internal" in urls
    assert "https://other.com/external" not in urls

@patch("crawler.fetcher.requests.get")
def test_skips_non_html_urls(mock_get):
    html = """
    <html>
      <head><title>Non-HTML</title></head>
      <body>
        <a href="https://example.com/image.png">Image</a>
        <a href="https://example.com/doc.pdf">PDF</a>
        <a href="https://example.com/page">Page</a>
      </body>
    </html>
    """
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.text = html
    mock_get.return_value = mock_response

    results = crawl("https://example.com", depth=1)
    urls = {page.url for page in results}

    assert "https://example.com" in urls
    assert "https://example.com/page" in urls
    assert "https://example.com/image.png" not in urls
    assert "https://example.com/doc.pdf" not in urls

@patch("crawler.fetcher.requests.get")
def test_handles_broken_links(mock_get):
    # Root page returns 200
    root_html = """
    <html>
      <head><title>Broken Link Test</title></head>
      <body>
        <h1>Main Page</h1>
        <a href="https://example.com/working">Good</a>
        <a href="https://example.com/broken">Bad</a>
      </body>
    </html>
    """

    def side_effect(url, timeout=5):
        mock = Mock()
        if url.endswith("/broken"):
            raise requests.exceptions.RequestException("Simulated failure")
        mock.status_code = 200
        mock.text = root_html if url == "https://example.com" else """
        <html><head><title>Child</title></head><body><h1>Child</h1></body></html>
        """
        return mock

    mock_get.side_effect = side_effect

    results = crawl("https://example.com", depth=1)
    urls = {page.url for page in results}

    assert "https://example.com" in urls
    assert "https://example.com/working" in urls
    assert "https://example.com/broken" not in urls  # Should be skipped

@patch("crawler.fetcher.requests.get")
def test_handles_missing_title_description_heading(mock_get):
    html = """
    <html>
      <head></head>
      <body>
        <p>No h1 here</p>
        <a href="https://example.com/page">Page</a>
      </body>
    </html>
    """
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.text = html
    mock_get.return_value = mock_response

@patch("crawler.fetcher.requests.get")
def test_allows_external_domain_when_enabled(mock_get):
    html = """
    <html>
      <head><title>External Test</title></head>
      <body>
        <a href="https://other.com/page">External Link</a>
      </body>
    </html>
    """
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.text = html
    mock_get.return_value = mock_response

    results = crawl("https://example.com", depth=1, allow_external=True)
    urls = {page.url for page in results}
    assert "https://example.com" in urls
    assert "https://other.com/page" in urls

@patch("crawler.fetcher.requests.get")
def test_blocks_external_domain_by_default(mock_get):
    html = """
    <html>
      <head><title>External Test</title></head>
      <body>
        <a href="https://other.com/page">External Link</a>
      </body>
    </html>
    """
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.text = html
    mock_get.return_value = mock_response

    results = crawl("https://example.com", depth=1)  # allow_external=False by default
    urls = {page.url for page in results}
    assert "https://example.com" in urls
    assert "https://other.com/page" not in urls

@patch("crawler.fetcher.requests.get")
def test_crawl_and_export_creates_json_file(mock_get):
    html = """
    <html>
      <head><title>Export Test</title></head>
      <body><h1>Hello</h1><a href="https://example.com/page">Page</a></body>
    </html>
    """
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.text = html
    mock_get.return_value = mock_response

    filename = "test_output.json"
    if os.path.exists(filename):
        os.remove(filename)

    crawl_and_export("https://example.com", depth=1, export_format="json", filename=filename)

    assert os.path.exists(filename)

    with open(filename, "r", encoding="utf-8") as f:
        data = json.load(f)
        assert isinstance(data, list)
        assert data[0]["url"] == "https://example.com"
        assert "title" in data[0]

    os.remove(filename)

 
