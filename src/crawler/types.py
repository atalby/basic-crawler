# In crawler/types.py

class PageData:
    def __init__(self, url: str, title: str, description: str, headings: list[str]):
        self.url = url
        self.title = title
        self.description = description
        self.headings = headings

    def model_dump(self):
        return {
            "url": self.url,
            "title": self.title,
            "description": self.description,
            "headings": self.headings,
        }

