from dataclasses import dataclass

@dataclass
class Message:
    author: str
    content: str


@dataclass
class SearchResult:
    name: str
    url: str
    snippet: str

    def get_passage(self) -> str:
        return self.url + "\n" + self.snippet

