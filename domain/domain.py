from dataclasses import dataclass
import os
from domain.domain_types import Annonce
import re
from contact import contact
from urllib.parse import urlparse

import requests
from dotenv import load_dotenv

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

        
def get_urls_from_mail_content(mailContent: str) -> set[str]:
    #print(content)
    pattern = r'https://www\.seloger\.com/annonces/[^ ]+'#/\d+\.htm'
    # Use the re.findall() function to extract all URLs that match the pattern
    links = set(re.findall(pattern, mailContent))

    urls = [ urlparse(link) for link in links]

    return [ url.scheme + "://" + url.netloc + url.path for url in urls ]

def answer_annonce(annonce: Annonce, contact: ContactInformation) -> requests.Response:
    s = requests.Session()

    s.headers.update({
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
    })
    
    payload = {
        "email": contact.email,
        "listingId": annonce.id,
        "listingPublicationId": 1,
        "message": contact.message,
        "name": contact.name,
        "phone": contact.phone
    }

    res = s.post("https://www.seloger.com/annoncesbff/2/Contact", json=payload)
    return res


def get_latest_annonces():
    

"""
def contact_agencies(urls: list[str], repository: AnnonceRepository, email: str, name: str, phone: str) -> None:

    contact_message = "Bonjour, je suis intéressé par cet appartement ! Prenez-vous actuellement des rendez-vous pour des visites ? Si oui, je suis intéressé. Je peux vous envoyer mon dossier par mail, et suis joignable au 0760912574. Vous pouvez également trouver mon dossier sur le site du gouvernement 'DossierFacile.fr' à cette adresse: https://locataire.dossierfacile.fr/file/b04472cd-9577-4115-a88f-22daa1a6ea30 . Bonne journée !"

    for url in urls:
        annonce = Annonce(url)

        id = extract_annonce_id_from_url(url)
        if not repository.annonce_exists(id):
            trySend = contact(id, email, contact_message, name, phone)
            if trySend.status_code == 200:
                print(f"contacted annonce: {id}  --> {url}")
                #print(trySend.content)
                repository.save_annonce(id, url)
        else:
            print(f"annonce: {id} already treated")


"""