import requests

def fetch_html(url: str, timeout: int = 5) -> str | None:
    try:
        response = requests.get(url, timeout=timeout)
        if response.status_code == 200:
            return response.text
    except requests.RequestException as e:
        print(f"[ERROR] Failed to fetch {url}: {e}")
    return None

