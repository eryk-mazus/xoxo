from dataclasses import dataclass

@dataclass
class Message:
    author: str
    content: str

@dataclass
class SearchResult:
    title: str
    url: str
    snippet: str

    def get_passage(self) -> str:
        return "url: " + self.url + "\n" + self.snippet