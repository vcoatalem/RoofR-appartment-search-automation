from dataclasses import dataclass
import re


@dataclass
class Annonce:
    def __init__(self, id: int, url: str) -> None:
        self.id = id
        self.url = url


def ParseAnnonceFromUrl(url: str) -> Annonce:

    def extract_annonce_id_from_url(url: str) -> int:
        extract_id_pattern = r"/(\d+)\.htm"
        match = re.search(pattern=extract_id_pattern, string=url)
        if match:
            number = int(match.group(1))
            return number
        return -1

    res = Annonce(
        id=extract_annonce_id_from_url(url),
        url=url
    )

    if res.id == -1:
        return None
    
    return res


@dataclass
class Mail():
    def __init__(self, sender: str, subject: str, content: str):
        self.sender = sender
        self.subject = subject
        self.content = content

    def is_annonce(self) -> bool:
        return "annonce" in self.subject