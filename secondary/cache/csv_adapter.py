import os
import csv
from domain.cache_port import CachePort
from domain.domain_types import Annonce

class CSVAdapter(CachePort):
    def __init__(self, filename: str) -> None:
        self.filename = filename
        super().__init__()

    @staticmethod
    def __annonce_from_csv(row):
        return Annonce(id=row[0], url=row[1])

    @staticmethod
    def __annonce_to_csv(annonce: Annonce) -> list[str]:
        return [annonce.id, annonce.url]

    def load(self) -> set[Annonce]:
        if not os.path.exists(self.filename):
            return []
        with open(self.filename, newline='', mode="r") as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                self.annonces.add(CSVAdapter.__annonce_from_csv(row))
        return self.annonces
    
    def save(self) -> bool:
        with open(self.filename, 'a', newline='') as file:
            writer = csv.writer(file)
            for annonce in self.annonces_to_save:
                writer.writerow(CSVAdapter.__annonce_to_csv(annonce))
        return True