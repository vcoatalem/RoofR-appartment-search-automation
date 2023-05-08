import csv
import os

from domain.cache_port import CachePort
from domain.domain_types import Annonce


class InMemoryAdapter(CachePort):
    def __init__(self, filename: str) -> None:
        self.filename = filename
        super().__init__()

    def load(self) -> set[Annonce]:
        print("MOCK Cache: load()")
        return set()
    
    def save(self) -> bool:
        print("MOCK cache: save")
        return True