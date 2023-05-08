from dataclasses import dataclass

from abc import ABC, abstractmethod

from domain.domain_types import Annonce, ContactInformation, Mail


class AnnonceAPIPort(ABC):

    @dataclass
    class Response:
        def __init__(self, annonce: Annonce, wasSent: bool, wasAccepted: bool, error: dict) -> None:
            self.annonce = annonce
            self.wasSent = wasSent
            self.wasAccepted = wasAccepted
            self.error = error


    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def contact(self, annonce: Annonce, contact: ContactInformation) -> Response:
        pass

    @abstractmethod
    def find_urls_in_mail(self, mail: Mail) -> set[str]:
        pass
        """
        pattern = r'https://www\.seloger\.com/annonces/[^ ]+'#/\d+\.htm'
        # Use the re.findall() function to extract all URLs that match the pattern
        links = set(re.findall(pattern, mailContent))

        urls = [ urlparse(link) for link in links]

        return [ url.scheme + "://" + url.netloc + url.path for url in urls ]
        """