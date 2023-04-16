import csv
from typing import Optional
from dataclasses import dataclass


@dataclass
class Annonce:
    filename = "annonces.csv"
    def __init__(self, id: int, url: str) -> None:
        self.id = id
        self.url = url

class AnnonceRepository:

    def __init__(self) -> None:
        self.annonces = None
        self.__load_annonces()

    def save_annonce(self, id, url) -> None:
        with open(Annonce.filename, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([id, url])
            self.annonces.append(Annonce(id, url))

    def __load_annonces(self) -> list[Annonce]:
        with open(Annonce.filename, newline='') as csvfile:
            reader = csv.reader(csvfile)
            data = []
            for row in reader:
                data.append(Annonce(row[0], row[1]))
            self.annonces = data
    
    def annonce_exists(self, id) -> bool:
        return any(int(annonce.id) == int(id) for annonce in self.annonces)




