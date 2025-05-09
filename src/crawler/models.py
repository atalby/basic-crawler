from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class PageData:
    url: str
    title: str
    description: Optional[str]
    headings: list[str]

