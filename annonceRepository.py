import csv
import os
from typing import Optional
from dataclasses import dataclass

from abc import ABC, abstractmethod

@dataclass
class Annonce:
    def __init__(self, id: int, url: str) -> None:
        self.id = id
        self.url = url

class AnnoncePersistance(ABC):

    @abstractmethod
    def load(self) -> list[Annonce]:
        pass

    @abstractmethod
    def save(self, id: str, url: str) -> bool:
        pass


class CSVPersistance(AnnoncePersistance):
    def __init__(self, filename: str) -> None:
        self.filename = filename
        super().__init__()

    def load(self) -> list[Annonce]:
        with open(self.filename, newline='') as csvfile:
            reader = csv.reader(csvfile)
            data = []
            for row in reader:
                data.append(Annonce(row[0], row[1]))
        self.annonces = data
        return data
    
    def save(self, id, url) -> bool:
        if not os.path.exists(self.filename) or not os.access(self.filename, os.R_OK):
            return False
        with open(self.filename, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([id, url])
            self.annonces.append(Annonce(id, url))
        return True


class AnnonceRepository:

    def __init__(self, persistor: AnnoncePersistance) -> None:
        self.annonces = None
        self.persistor = persistor
        self.annonces = self.persistor.load()

    @staticmethod
    def Basic():
        return AnnonceRepository(CSVPersistance("annonces.csv"))

    def save_annonce(self, id, url) -> None:
        tryAdd: bool = self.persistor.save(id, url)
        if tryAdd:
            self.annonces.append(Annonce(id, url))
  
    def annonce_exists(self, id) -> bool:
        return any(int(annonce.id) == int(id) for annonce in self.annonces)
    





