from bs4 import BeautifulSoup


class Document:
    def __init__(self, id: str, content: str, title: str, link: str = None):
        self.id = id
        self.content = content
        self.title = title
        self.link = link

    def raw_text(self) -> str:
        return BeautifulSoup(self.content, 'html.parser').get_text(strip=True)
