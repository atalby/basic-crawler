from urllib.parse import urlparse
from pathlib import Path

SKIP_EXTENSIONS = {
    ".png", ".jpg", ".jpeg", ".gif", ".svg", ".bmp", ".ico",
    ".pdf", ".xml", ".psd", ".zip", ".rar", ".7z", ".tar", ".gz", ".exe",
    ".dmg", ".iso", ".mp3", ".mp4", ".avi", ".mkv"
}

def should_skip_url(url: str) -> bool:
    return Path(urlparse(url).path).suffix.lower() in SKIP_EXTENSIONS

