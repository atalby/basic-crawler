from dataclasses import dataclass

@dataclass
class PageData:
    url: str
    title: str
    description: str
    headings: list[str]

