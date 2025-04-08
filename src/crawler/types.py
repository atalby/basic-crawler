from dataclasses import dataclass

@dataclass(frozen=True)
class PageData:
    url: str
    title: str
    description: str
    headings: list[str]

