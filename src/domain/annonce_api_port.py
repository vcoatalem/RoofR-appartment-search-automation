from abc import ABC, abstractmethod
from dataclasses import dataclass

from src.domain.domain_types import Annonce, ContactInformation, Mail


class AnnonceAPIPort(ABC):

    @dataclass
    class Response:
        def __init__(self, annonce: Annonce, wasSent: bool = False, wasAccepted: bool = False, isOutdated: bool = False, error: dict = {}) -> None:
            self.annonce = annonce
            self.wasSent = wasSent
            self.wasAccepted = wasAccepted
            self.isOutdated = isOutdated
            self.error = error

        def __repr__(self):
            if (self.wasAccepted):
                return "AnnonceAPIPort.Response(Success)"
            if (self.wasSent):
                return "AnnonceAPIPort.Response(Failure)"
            return "AnnonceAPIPort.Response(Network Error)"

    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def contact(self, annonce: Annonce, contact: ContactInformation) -> Response:
        pass

    @abstractmethod
    def find_urls_in_mail(self, mail: Mail) -> set[str]:
        pass
