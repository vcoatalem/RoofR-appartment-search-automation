from dataclasses import dataclass
import re
import os
from dotenv import load_dotenv


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
    
    def __repr__(self):
        return f"mail from sender: {self.sender} with subject: {self.subject}"
    
@dataclass
class ContactInformation:

    def __init__(self, email: str, name: str, phone: str, message: str):
        self.email = email
        self.name = name
        self.phone = phone
        self.message = message

    @staticmethod
    def from_env():
        load_dotenv()
        email = os.getenv("FROM_EMAIL")
        name = os.getenv("NAME")
        phone = os.getenv("PHONE")
        message = "Bonjour, je suis intéressé par cet appartement ! Prenez-vous actuellement des rendez-vous pour des visites ? Si oui, je suis intéressé. Je peux vous envoyer mon dossier par mail, et suis joignable au 0760912574. Vous pouvez également trouver mon dossier sur le site du gouvernement 'DossierFacile.fr' à cette adresse: https://locataire.dossierfacile.fr/file/b04472cd-9577-4115-a88f-22daa1a6ea30 . Bonne journée !"
        return ContactInformation(
            email=email,
            name=name,
            phone=phone,
            message=message
        )