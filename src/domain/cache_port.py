from abc import ABC, abstractmethod

from src.domain.domain_types import Annonce


class CachePort(ABC):

    def __init__(self) -> None:
        super().__init__()
        self.annonces: set[Annonce] = set()
        self.annonces_to_save: set[Annonce] = set()

    @abstractmethod
    def load(self) -> set[Annonce]:
        pass

    @abstractmethod
    def save() -> bool:
        pass

    def add(self, annonce: Annonce):
        if annonce not in self.annonces:
            self.annonces.add(annonce)
            self.annonces_to_save.add(annonce)

    def contains(self, ann: Annonce):
        return ann in self.annonces


