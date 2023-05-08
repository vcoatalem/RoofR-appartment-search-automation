from dataclasses import dataclass
import re
import os
from dotenv import load_dotenv


@dataclass
class Annonce:
    def __init__(self, id: str, url: str) -> None:
        self.id = id
        self.url = url

    @staticmethod
    def __extract_id_from_url(url: str) -> str:
        extract_id_pattern = r"/(\d+)\.htm"
        match = re.search(pattern=extract_id_pattern, string=url)
        if match:
            number = match.group(1)
            return number
        return None

    @staticmethod
    def from_url(url: str):
        res = Annonce(
                id=Annonce.__extract_id_from_url(url),
                url=url
            )
        if not res.id:
            return None
        return res
    
    def __repr__(self):
        return "Annonce(" + self.url + ")"

    def __hash__(self):
        return hash(self.url)

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