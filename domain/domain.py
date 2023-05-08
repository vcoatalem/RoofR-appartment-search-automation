from dataclasses import dataclass
import os
from domain.domain_types import Annonce, Mail, ContactInformation
from domain.inbox_port import InboxPort
from domain.cache_port import CachePort
from domain.annonce_api_port import AnnonceAPIPort
import re
from old.contact import contact

import requests
from dotenv import load_dotenv


"""
def get_urls_from_mail_content(mailContent: str) -> set[str]:
    #print(content)
    pattern = r'https://www\.seloger\.com/annonces/[^ ]+'#/\d+\.htm'
    # Use the re.findall() function to extract all URLs that match the pattern
    links = set(re.findall(pattern, mailContent))

    urls = [ urlparse(link) for link in links]

    return [ url.scheme + "://" + url.netloc + url.path for url in urls ]
"""

"""
def contact_agency(annonce: Annonce, contact: ContactInformation) -> requests.Response:
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
    return s.post("https://www.seloger.com/annoncesbff/2/Contact", json=payload)
"""

def get_latest_agency_mails(inbox: InboxPort, read: bool = False) -> list[Mail]:
    mails : list[Mail] = inbox.peekUnreadMails() if not read else inbox.readUnreadMails()
    annonces = [ mail for mail in mails if mail.is_annonce() ]
    return annonces

def extract_annonces_from_one_mail(mail: Mail, api: AnnonceAPIPort, cache: CachePort) -> set[Annonce]:
    urls = api.find_urls_in_mail(mail)
    annonces = [ Annonce.from_url(url) for url in urls ]
    annonces = [ x for x in filter(lambda annonce: not cache.contains(annonce), annonces)]
    return set(annonces)

def extract_annonces_from_all_mails(mails: list[Mail], api: AnnonceAPIPort, cache: CachePort) -> set[Annonce]:
    set_list = [ extract_annonces_from_one_mail(mail, api, cache) for mail in mails ]
    return set().union(*set_list)

def answer_annonce(annonce: Annonce, api: AnnonceAPIPort, cache: CachePort, contact: ContactInformation) -> requests.Response:
    response = api.contact(annonce, contact)
    if response.status_code == 200:
        print(f"contacted agency for annonce with url : `{annonce.url}`")
        cache.add(annonce)
    return response


def answer_all_annonces(inbox: InboxPort, cache: CachePort, api: AnnonceAPIPort, contact: ContactInformation) -> list[requests.Response]:
    mails = get_latest_agency_mails(inbox, read=False)
    print(f"found {len(mails)} mails")
    annonces = extract_annonces_from_all_mails(mails, api, cache)
    print(f"found {len(annonces)} annonces")
    responses = [ response for response in map(lambda annonce: answer_annonce(annonce, api, cache, contact), annonces)]
    cache.save()
    return responses



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